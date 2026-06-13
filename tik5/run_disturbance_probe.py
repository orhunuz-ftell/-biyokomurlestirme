"""TIK-5 bozucu etki teshis + senaryo sondaji.

Prensip: model yeniden EGITILMEZ. Kayitli forward surrogate ve reverse soft-sensor
yuklenir; yalnizca senaryo parametreleri (hedef H2/CO, baslangic koşulu, bozucu yön/
buyukluk) degistirilerek davranis olculur. Sonuclar JSON olarak yazilir.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

MPC_ROOT = Path(r"C:\@biyokomurlestirme\reverse_ml_biooil_to_product\optimization_control_mpc")
SRC_DIR = MPC_ROOT / "src"
sys.path.insert(0, str(SRC_DIR))

from common import DATA_PATH, PROCESS_FEATURES, SYNGAS_FEATURES, TARGET_FEATURES  # noqa: E402
from surrogate_model import ForwardSurrogate, add_h2_co_ratio  # noqa: E402
from optimization import ProcessOptimizer  # noqa: E402
from mpc_controller import SimpleMPCController  # noqa: E402
from inverse_predictor import ReverseMLSoftSensor  # noqa: E402

# Keras 3, eski h5 modelini derlenmis loss ('mse') ile yukleyemiyor. Cikarim icin
# derleme gerekmez; kaynak dosyayi degistirmeden load_model'i compile=False yapariz.
import tensorflow as _tf  # noqa: E402
_orig_load = _tf.keras.models.load_model
_tf.keras.models.load_model = lambda *a, **k: _orig_load(*a, **{**k, "compile": False})

INTERIOR = {"Reformer_Temperature_C": 750.0, "Reformer_Pressure_bar": 15.0, "Steam_to_Carbon_Ratio": 4.0}


def load_unique_compositions(df):
    return df.groupby("BiooilID")[TARGET_FEATURES].first().reset_index()


def renorm(series):
    s = series.clip(lower=0.0)
    return s / s.sum() * 100.0


# ---------- PART A: duyarlilik sondaji ----------
def sensitivity_probe(surrogate, df):
    comps = load_unique_compositions(df)
    cond_df = pd.DataFrame([INTERIOR])
    ratios = []
    for _, row in comps.iterrows():
        biooil = row[TARGET_FEATURES]
        pred = surrogate.predict_many(biooil, cond_df)
        ratios.append(float(pred["H2_CO_Ratio"].iloc[0]))
    ratios = np.array(ratios)
    ratios = ratios[np.isfinite(ratios)]

    # One-at-a-time: dengeli bir taban kompozisyon, her bilesen min->max
    base = comps[TARGET_FEATURES].mean()
    feat_ranges = {}
    for feat in TARGET_FEATURES:
        lo = float(df[feat].quantile(0.05))
        hi = float(df[feat].quantile(0.95))
        sweep = []
        for val in np.linspace(lo, hi, 9):
            comp = base.copy()
            comp[feat] = val
            comp = renorm(comp)
            pred = surrogate.predict_many(comp, cond_df)
            sweep.append(float(pred["H2_CO_Ratio"].iloc[0]))
        sweep = np.array(sweep)
        feat_ranges[feat] = {
            "lo_pct": lo, "hi_pct": hi,
            "H2CO_min": float(np.nanmin(sweep)), "H2CO_max": float(np.nanmax(sweep)),
            "delta": float(np.nanmax(sweep) - np.nanmin(sweep)),
        }

    # mpc_controller'daki bozucu yon boyunca (asit+, aromatik-, fenol-) buyutulmus
    dir_sweep = []
    base_bal = comps.copy()
    base_bal["spread"] = comps[TARGET_FEATURES].std(axis=1)
    balanced = base_bal.sort_values("spread").iloc[0][TARGET_FEATURES]
    for scale in [0, 1, 2, 3, 4]:
        comp = balanced.copy()
        comp["Biooil_Acids_pct"] += 8.0 * scale
        comp["Biooil_Aromatics_pct"] -= 6.0 * scale
        comp["Biooil_Phenols_pct"] -= 2.0 * scale
        comp = renorm(comp)
        pred = surrogate.predict_many(comp, pd.DataFrame([INTERIOR]))
        dir_sweep.append({"scale": scale, "H2CO": float(pred["H2_CO_Ratio"].iloc[0])})

    return {
        "interior_conditions": INTERIOR,
        "n_compositions": int(len(ratios)),
        "dataset_sweep": {
            "H2CO_min": float(np.min(ratios)), "H2CO_max": float(np.max(ratios)),
            "H2CO_mean": float(np.mean(ratios)), "H2CO_std": float(np.std(ratios)),
            "delta_max": float(np.max(ratios) - np.min(ratios)),
        },
        "per_feature_one_at_a_time": feat_ranges,
        "disturbance_direction_sweep": dir_sweep,
    }


# ---------- PART B: senaryo karsilastirmasi (kapali cevrim) ----------
def run_scenario(soft_sensor, surrogate, df, target, start_conditions, start_case,
                 dist_step=5, steps=10, dist=("Biooil_Acids_pct", 8.0)):
    cases = load_unique_compositions(df)
    cases["spread"] = cases[TARGET_FEATURES].std(axis=1)
    if start_case == "balanced":
        bid = cases.sort_values("spread").iloc[0]["BiooilID"]
    elif start_case == "aromatic_rich":
        bid = cases.sort_values("Biooil_Aromatics_pct", ascending=False).iloc[0]["BiooilID"]
    elif start_case == "acid_rich":
        bid = cases.sort_values("Biooil_Acids_pct", ascending=False).iloc[0]["BiooilID"]
    initial_biooil = df[df["BiooilID"] == bid].iloc[0][TARGET_FEATURES]

    mpc = SimpleMPCController(soft_sensor, surrogate, target_h2_co=target)
    out = mpc.run(initial_biooil, start_conditions, steps=steps, disturbance_step=dist_step)

    m = out["measured_H2_CO_Ratio"]
    pre = float(m.iloc[dist_step - 1])
    at = float(m.iloc[dist_step])
    recovered = float(m.iloc[-1])
    # kontrol degiskeni hareketi (uygulanan koşullar uzerinden)
    moves = {}
    for col in PROCESS_FEATURES:
        applied = out[f"applied_{col}"]
        moves[col] = {
            "pre": float(applied.iloc[dist_step]),
            "post": float(applied.iloc[-1]),
            "changed": bool(abs(applied.iloc[-1] - applied.iloc[dist_step]) > 1e-6),
            "n_unique": int(applied.round(6).nunique()),
        }
    return {
        "target_h2_co": target,
        "start_conditions": start_conditions,
        "start_case": start_case,
        "start_BiooilID": int(bid),
        "disturbance": {"feature": dist[0], "delta": dist[1]},
        "measured_H2CO": {"pre_disturbance": pre, "at_disturbance": at, "recovered": recovered,
                          "dip_from_pre": at - pre, "recovery_gap": recovered - target},
        "control_moves": moves,
        "final_objective": float(out["objective"].iloc[-1]),
        "final_energy_cost": float(out["next_energy_cost"].iloc[-1]),
    }


def main():
    df = add_h2_co_ratio(pd.read_csv(DATA_PATH))
    print("surrogate yukleniyor (egitim yok)...")
    surrogate = ForwardSurrogate.load()

    print("PART A: duyarlilik sondaji...")
    probe = sensitivity_probe(surrogate, df)

    print("soft-sensor yukleniyor (egitim yok)...")
    soft_sensor = ReverseMLSoftSensor()

    print("PART B: senaryolar...")
    scenarios = []
    CORNER = {"Reformer_Temperature_C": 750.0, "Reformer_Pressure_bar": 15.0, "Steam_to_Carbon_Ratio": 4.0}
    # V0: mevcut varsayilan (hedef 2.0, balanced)
    scenarios.append(("V0_baseline_t2.0_balanced",
                      run_scenario(soft_sensor, surrogate, df, 2.0, CORNER, "balanced")))
    # V1: hedef 2.5 (kilit acma denemesi)
    scenarios.append(("V1_t2.5_balanced",
                      run_scenario(soft_sensor, surrogate, df, 2.5, CORNER, "balanced")))
    # V2: hedef 2.5 + aromatik-zengin baslangic
    scenarios.append(("V2_t2.5_aromatic_rich",
                      run_scenario(soft_sensor, surrogate, df, 2.5, CORNER, "aromatic_rich")))
    # V3: hedef 2.5 + asit-zengin + buyuk asit bozucu
    scenarios.append(("V3_t2.5_acid_rich_bigdist",
                      run_scenario(soft_sensor, surrogate, df, 2.5, CORNER, "acid_rich",
                                   dist=("Biooil_Acids_pct", 20.0))))

    result = {"part_A_sensitivity": probe,
              "part_B_scenarios": {name: data for name, data in scenarios}}

    out_json = Path(r"C:\@biyokomurlestirme\tik5\TIK5_DISTURBANCE_PROBE_RESULTS.json")
    out_json.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("YAZILDI:", out_json)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
