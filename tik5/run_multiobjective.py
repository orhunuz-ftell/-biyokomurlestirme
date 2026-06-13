"""TIK-5 cok-amacli (agirlikli toplam) optimizasyon — kompozisyon bozucusu korunur.

Prensip: model yeniden EGITILMEZ. Kayitli forward surrogate + reverse soft-sensor
yuklenir. Resmi optimization.py degistirilmez; cok-amacli amac burada tanimlanir.

Amac:
  J = w_ratio*(H2/CO sapma)^2 + w_h2*(H2 acigi) + w_ch4*(CH4 kaymasi)
    + w_co2*(CO2) + w_energy*(enerji) + w_coke*(koklasma riski)
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

MPC_ROOT = Path(r"C:\@biyokomurlestirme\reverse_ml_biooil_to_product\optimization_control_mpc")
SRC_DIR = MPC_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from common import PROCESS_FEATURES, SYNGAS_FEATURES, TARGET_FEATURES  # noqa: E402
from surrogate_model import ForwardSurrogate, add_h2_co_ratio, DATA_PATH  # noqa: E402
from optimization import energy_cost  # noqa: E402

import tensorflow as _tf  # noqa: E402
_orig_load = _tf.keras.models.load_model
_tf.keras.models.load_model = lambda *a, **k: _orig_load(*a, **{**k, "compile": False})
from inverse_predictor import ReverseMLSoftSensor  # noqa: E402

# --- normalizasyon referanslari (amac terimlerini ~[0,1] olceginde tutmak icin) ---
H2_REF = 50.0     # arzu edilen H2 mol% tavani
CH4_REF = 5.0     # CH4 kaymasi olcegi
CO2_REF = 16.0    # CO2 olcegi (mevcut max_co2 ile uyumlu)

DEFAULT_WEIGHTS = {
    "ratio": 4.0,
    "h2": 3.0,
    "ch4": 2.0,
    "co2": 1.0,
    "energy": 1.5,
    "coke": 1.5,
    "move": 0.0,
}


def candidate_grid():
    rows = []
    for t in [650, 675, 700, 725, 750, 775, 800, 825, 850]:
        for p in [5, 10, 15, 20, 25, 30]:
            for sc in [2.0, 3.0, 4.0, 5.0, 6.0]:
                rows.append({"Reformer_Temperature_C": float(t),
                             "Reformer_Pressure_bar": float(p),
                             "Steam_to_Carbon_Ratio": float(sc)})
    return pd.DataFrame(rows)


def coking_risk(t, sc):
    """Koklasma proxy: yuksek T + dusuk S/C -> yuksek risk, ~[0,1]."""
    t_term = np.clip((t - 700.0) / 150.0, 0.0, 1.0)
    sc_term = np.clip((4.0 - sc) / 2.0, 0.0, 1.0)
    return t_term * sc_term


def objective_terms(syngas, candidates, target, previous=None):
    ratio = ((syngas["H2_CO_Ratio"] - target) / target) ** 2
    h2_def = (H2_REF - syngas["H2_molpercent"]).clip(lower=0.0) / H2_REF
    ch4 = syngas["CH4_molpercent"] / CH4_REF
    co2 = syngas["CO2_molpercent"] / CO2_REF
    energy = candidates.apply(lambda r: energy_cost(r["Reformer_Temperature_C"],
                                                    r["Reformer_Pressure_bar"],
                                                    r["Steam_to_Carbon_Ratio"]), axis=1)
    coke = candidates.apply(lambda r: coking_risk(r["Reformer_Temperature_C"],
                                                  r["Steam_to_Carbon_Ratio"]), axis=1)
    move = pd.Series(0.0, index=candidates.index)
    if previous is not None:
        move = (((candidates["Reformer_Temperature_C"] - previous["Reformer_Temperature_C"]) / 200.0) ** 2
                + ((candidates["Reformer_Pressure_bar"] - previous["Reformer_Pressure_bar"]) / 25.0) ** 2
                + ((candidates["Steam_to_Carbon_Ratio"] - previous["Steam_to_Carbon_Ratio"]) / 4.0) ** 2) / 3.0
    return {"ratio": ratio, "h2": h2_def, "ch4": ch4, "co2": co2,
            "energy": energy.reset_index(drop=True), "coke": coke.reset_index(drop=True),
            "move": move}


class MultiObjectiveOptimizer:
    def __init__(self, surrogate, target=2.5, weights=None):
        self.surrogate = surrogate
        self.target = target
        self.w = dict(DEFAULT_WEIGHTS)
        if weights:
            self.w.update(weights)

    def optimize(self, biooil, previous=None):
        cand = candidate_grid()
        syn = self.surrogate.predict_many(biooil, cand).reset_index(drop=True)
        terms = objective_terms(syn, cand, self.target, previous)
        J = sum(self.w[k] * terms[k] for k in terms)
        idx = int(J.idxmin())
        chosen = {c: float(cand.loc[idx, c]) for c in PROCESS_FEATURES}
        term_vals = {k: float(terms[k].loc[idx]) for k in terms}
        weighted = {k: float(self.w[k] * terms[k].loc[idx]) for k in terms}
        return {
            "conditions": chosen,
            "objective": float(J.loc[idx]),
            "syngas": {c: float(syn.loc[idx, c]) for c in SYNGAS_FEATURES},
            "H2_CO_Ratio": float(syn.loc[idx, "H2_CO_Ratio"]),
            "term_raw": term_vals,
            "term_weighted": weighted,
        }


def representative_biooils(df):
    g = df.groupby("BiooilID")[TARGET_FEATURES].first().reset_index()
    g["spread"] = g[TARGET_FEATURES].std(axis=1)
    return {
        "balanced": int(g.sort_values("spread").iloc[0]["BiooilID"]),
        "aromatic_rich": int(g.sort_values("Biooil_Aromatics_pct", ascending=False).iloc[0]["BiooilID"]),
        "acid_rich": int(g.sort_values("Biooil_Acids_pct", ascending=False).iloc[0]["BiooilID"]),
    }


def static_compare(surrogate, df, target=2.5):
    """Tek-amacli (sadece oran) vs cok-amacli optimum karsilastirmasi."""
    ids = representative_biooils(df)
    single = MultiObjectiveOptimizer(surrogate, target,
                                     weights={"ratio": 8.0, "h2": 0, "ch4": 0,
                                              "co2": 0, "energy": 0, "coke": 0})
    multi = MultiObjectiveOptimizer(surrogate, target)
    out = {}
    for name, bid in ids.items():
        biooil = df[df["BiooilID"] == bid].iloc[0][TARGET_FEATURES]
        out[name] = {"BiooilID": bid,
                     "single_objective": single.optimize(biooil),
                     "multi_objective": multi.optimize(biooil)}
    return out


def closed_loop(soft_sensor, surrogate, df, target=2.5, steps=10, dist_step=5):
    """Kompozisyon bozucusu korunur (asit+8, aromatik-6, fenol-2)."""
    ids = representative_biooils(df)
    biooil = df[df["BiooilID"] == ids["balanced"]].iloc[0][TARGET_FEATURES].copy()
    cond = {"Reformer_Temperature_C": 750.0, "Reformer_Pressure_bar": 15.0, "Steam_to_Carbon_Ratio": 4.0}
    opt = MultiObjectiveOptimizer(surrogate, target, weights={"move": 0.25})
    actual = pd.Series(biooil).copy()
    rec = []
    for step in range(steps):
        if step == dist_step:
            actual = actual.copy()
            actual["Biooil_Acids_pct"] += 8.0
            actual["Biooil_Aromatics_pct"] -= 6.0
            actual["Biooil_Phenols_pct"] -= 2.0
            actual = (actual.clip(lower=0.0) / actual.clip(lower=0.0).sum()) * 100.0
        measured = surrogate.predict(actual, cond)
        meas_row = {**cond, **{c: measured[c] for c in SYNGAS_FEATURES}}
        est = soft_sensor.predict(pd.DataFrame([meas_row]))[TARGET_FEATURES].iloc[0]
        res = opt.optimize(est, previous=cond)
        rec.append({
            "step": step,
            "measured_H2_CO": float(measured["H2_CO_Ratio"]),
            "measured_H2": float(measured["H2_molpercent"]),
            "measured_CO2": float(measured["CO2_molpercent"]),
            "measured_CH4": float(measured["CH4_molpercent"]),
            "applied_T": cond["Reformer_Temperature_C"],
            "applied_P": cond["Reformer_Pressure_bar"],
            "applied_SC": cond["Steam_to_Carbon_Ratio"],
            "next_T": res["conditions"]["Reformer_Temperature_C"],
            "next_P": res["conditions"]["Reformer_Pressure_bar"],
            "next_SC": res["conditions"]["Steam_to_Carbon_Ratio"],
            "objective": res["objective"],
            "term_weighted": res["term_weighted"],
        })
        cond = res["conditions"]
    return rec


def main():
    df = add_h2_co_ratio(pd.read_csv(DATA_PATH))
    print("surrogate yukleniyor (egitim yok)...")
    surrogate = ForwardSurrogate.load()
    print("statik karsilastirma (tek vs cok amacli)...")
    static = static_compare(surrogate, df, target=2.5)
    print("soft-sensor yukleniyor...")
    soft = ReverseMLSoftSensor()
    print("kapali cevrim (kompozisyon bozucusu)...")
    loop = closed_loop(soft, surrogate, df, target=2.5)

    result = {"weights": DEFAULT_WEIGHTS,
              "normalization": {"H2_REF": H2_REF, "CH4_REF": CH4_REF, "CO2_REF": CO2_REF},
              "static_single_vs_multi": static,
              "closed_loop_composition_disturbance": loop}
    out = Path(r"C:\@biyokomurlestirme\tik5\TIK5_MULTIOBJECTIVE_RESULTS.json")
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("YAZILDI:", out)


if __name__ == "__main__":
    main()
