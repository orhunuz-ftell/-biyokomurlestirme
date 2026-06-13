"""TIK-5 4-adimli case study — KOMPOZISYONA BAGLI koklasma terimi (Fikir B).

Yeni: koklasma cezasi kok-oncul fraksiyonu phi=(aromatik+fenol)/100 ile carpilir.
Boylece kompozisyon degisince optimum T/S-C degisir. Model yeniden EGITILMEZ;
kayitli surrogate. Statik, soft-sensor gerekmez.
"""

import json
import sys
from pathlib import Path

import numpy as np
import pandas as pd

MPC_ROOT = Path(r"C:\@biyokomurlestirme\reverse_ml_biooil_to_product\optimization_control_mpc")
sys.path.insert(0, str(MPC_ROOT / "src"))
from common import TARGET_FEATURES, SYNGAS_FEATURES, PROCESS_FEATURES  # noqa: E402
from surrogate_model import ForwardSurrogate, add_h2_co_ratio, DATA_PATH  # noqa: E402
from optimization import energy_cost  # noqa: E402

TARGET = 2.5
H2_REF, CH4_REF, CO2_REF = 50.0, 5.0, 16.0
WEIGHTS = {"ratio": 4.0, "h2": 3.0, "ch4": 2.0, "co2": 1.0, "energy": 1.5, "coke": 8.0}


def grid():
    rows = []
    for t in [650, 675, 700, 725, 750, 775, 800, 825, 850]:
        for p in [5, 10, 15, 20, 25, 30]:
            for sc in [2.0, 3.0, 4.0, 5.0, 6.0]:
                rows.append({"Reformer_Temperature_C": float(t),
                             "Reformer_Pressure_bar": float(p),
                             "Steam_to_Carbon_Ratio": float(sc)})
    return pd.DataFrame(rows)


def phi_coke(biooil):
    """Kok-oncul fraksiyonu: aromatik + fenol."""
    return float(biooil["Biooil_Aromatics_pct"] + biooil["Biooil_Phenols_pct"]) / 100.0


def coke_shape(t, sc):
    t_term = np.clip((t - 700.0) / 150.0, 0.0, 1.0)
    sc_term = np.clip((4.0 - sc) / 2.0, 0.0, 1.0)
    return t_term * sc_term


def evaluate(surrogate, biooil, cand):
    """Tum aday kosullar icin amac terimleri (koklasma kompozisyona bagli)."""
    syn = surrogate.predict_many(biooil, cand).reset_index(drop=True)
    phi = phi_coke(biooil)
    ratio = ((syn["H2_CO_Ratio"] - TARGET) / TARGET) ** 2
    h2 = (H2_REF - syn["H2_molpercent"]).clip(lower=0.0) / H2_REF
    ch4 = syn["CH4_molpercent"] / CH4_REF
    co2 = syn["CO2_molpercent"] / CO2_REF
    energy = cand.apply(lambda r: energy_cost(r["Reformer_Temperature_C"], r["Reformer_Pressure_bar"],
                                              r["Steam_to_Carbon_Ratio"]), axis=1).reset_index(drop=True)
    coke = cand.apply(lambda r: phi * coke_shape(r["Reformer_Temperature_C"],
                                                 r["Steam_to_Carbon_Ratio"]), axis=1).reset_index(drop=True)
    terms = {"ratio": ratio, "h2": h2, "ch4": ch4, "co2": co2, "energy": energy, "coke": coke}
    J = sum(WEIGHTS[k] * terms[k] for k in terms)
    return syn, terms, J, phi


def optimize(surrogate, biooil):
    cand = grid()
    syn, terms, J, phi = evaluate(surrogate, biooil, cand)
    i = int(J.idxmin())
    return {
        "conditions": {c: float(cand.loc[i, c]) for c in PROCESS_FEATURES},
        "H2_CO_Ratio": float(syn.loc[i, "H2_CO_Ratio"]),
        "H2": float(syn.loc[i, "H2_molpercent"]), "CO2": float(syn.loc[i, "CO2_molpercent"]),
        "CH4": float(syn.loc[i, "CH4_molpercent"]),
        "objective": float(J.loc[i]), "phi_coke": phi,
        "term_weighted": {k: float(WEIGHTS[k] * terms[k].loc[i]) for k in terms},
        "_idx": i,
    }


def eval_at_conditions(surrogate, biooil, conditions):
    cand = pd.DataFrame([conditions])
    syn, terms, J, phi = evaluate(surrogate, biooil, cand)
    return {
        "conditions": conditions, "H2_CO_Ratio": float(syn.loc[0, "H2_CO_Ratio"]),
        "objective": float(J.loc[0]), "phi_coke": phi,
        "term_weighted": {k: float(WEIGHTS[k] * terms[k].loc[0]) for k in terms},
    }


def disturb_to_aromatic(biooil):
    """Besleme kok-oncullerince ZENGINLESIR: aromatik+10, fenol+20 puan."""
    b = biooil.copy()
    b["Biooil_Aromatics_pct"] += 15.0
    b["Biooil_Phenols_pct"] += 35.0
    b = b.clip(lower=0.0)
    return b / b.sum() * 100.0


def comp(biooil):
    return {c.replace("Biooil_", "").replace("_pct", ""): round(float(biooil[c]), 2) for c in TARGET_FEATURES}


def main():
    df = add_h2_co_ratio(pd.read_csv(DATA_PATH))
    surrogate = ForwardSurrogate.load()

    # Baslangic: en DUSUK kok-oncullu temsili biyoyag (optimum sicak/kuru baslasin)
    g = df.groupby("BiooilID")[TARGET_FEATURES].first().reset_index()
    g["phi"] = (g["Biooil_Aromatics_pct"] + g["Biooil_Phenols_pct"]) / 100.0
    bid = int(g.sort_values("phi").iloc[0]["BiooilID"])
    biooil0 = df[df["BiooilID"] == bid].iloc[0][TARGET_FEATURES]

    res0 = optimize(surrogate, biooil0)            # ADIM 2
    biooil1 = disturb_to_aromatic(biooil0)         # ADIM 3 bozucu
    at_old = eval_at_conditions(surrogate, biooil1, res0["conditions"])
    res1 = optimize(surrogate, biooil1)            # ADIM 4

    moved = {c: (res0["conditions"][c], res1["conditions"][c],
                 abs(res1["conditions"][c] - res0["conditions"][c]) > 1e-6) for c in PROCESS_FEATURES}

    result = {
        "step1_objective": {"weights": WEIGHTS, "target_h2_co": TARGET,
            "coking_term": "w_coke * phi(komp) * coke_shape(T,S/C), phi=(aromatik+fenol)/100"},
        "biooil_start": {"BiooilID": bid, "composition": comp(biooil0), "phi_coke": round(res0["phi_coke"], 3)},
        "step2_optimum_before": {
            "conditions": res0["conditions"], "H2_CO": round(res0["H2_CO_Ratio"], 3),
            "objective": round(res0["objective"], 3),
            "coke_term": round(res0["term_weighted"]["coke"], 3),
            "term_weighted": {k: round(v, 3) for k, v in res0["term_weighted"].items()}},
        "step3_disturbance": {
            "disturbed_composition": comp(biooil1),
            "phi_before": round(res0["phi_coke"], 3), "phi_after": round(at_old["phi_coke"], 3),
            "at_old_optimum": {
                "conditions": at_old["conditions"], "H2_CO": round(at_old["H2_CO_Ratio"], 3),
                "objective_jumped_to": round(at_old["objective"], 3),
                "coke_term_jumped_to": round(at_old["term_weighted"]["coke"], 3)},
            "objective_increase": round(at_old["objective"] - res0["objective"], 3)},
        "step4_reoptimized": {
            "conditions": res1["conditions"], "H2_CO": round(res1["H2_CO_Ratio"], 3),
            "objective": round(res1["objective"], 3),
            "coke_term": round(res1["term_weighted"]["coke"], 3),
            "term_weighted": {k: round(v, 3) for k, v in res1["term_weighted"].items()}},
        "optimum_shift": moved,
    }
    out = Path(__file__).resolve().parent / "TIK5_CASE_STUDY_COKING_RESULTS.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("YAZILDI:", out)
    print(json.dumps(result["optimum_shift"], indent=2))


if __name__ == "__main__":
    main()
