"""TIK-5 4-adimli case study: amac -> optimum -> bozucu -> yeniden optimum.

Sabit agirlik seti. Model yeniden EGITILMEZ; kayitli surrogate yuklenir.
Bozucu etki KOMPOZISYONDA (kullanicinin secimi). Optimumun gercekten kayip
kaymadigini dogrudan test eder (standart 8-puan ve buyutulmus 24-puan bozucu).
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_multiobjective import (  # noqa: E402  (TF burada yuklenir ama kullanilmaz)
    MultiObjectiveOptimizer, DEFAULT_WEIGHTS, representative_biooils,
    objective_terms, candidate_grid,
)
from surrogate_model import ForwardSurrogate, add_h2_co_ratio, DATA_PATH  # noqa: E402
from common import TARGET_FEATURES, SYNGAS_FEATURES, PROCESS_FEATURES  # noqa: E402

TARGET = 2.5
WEIGHTS = {k: v for k, v in DEFAULT_WEIGHTS.items()}  # sabit set


def disturb(biooil, scale=1.0):
    """Kompozisyon bozucusu: asit+, aromatik-, fenol- (scale ile buyutulur)."""
    b = biooil.copy()
    b["Biooil_Acids_pct"] += 8.0 * scale
    b["Biooil_Aromatics_pct"] -= 6.0 * scale
    b["Biooil_Phenols_pct"] -= 2.0 * scale
    b = b.clip(lower=0.0)
    return b / b.sum() * 100.0


def eval_at(surrogate, biooil, conditions, target):
    """Verilen kompozisyon+kosulda sentez gazi ve amac degeri."""
    cand = pd.DataFrame([conditions])
    syn = surrogate.predict_many(biooil, cand).reset_index(drop=True)
    terms = objective_terms(syn, cand, target)
    J = sum(WEIGHTS[k] * terms[k] for k in terms)
    return {
        "conditions": conditions,
        "H2_CO_Ratio": float(syn.loc[0, "H2_CO_Ratio"]),
        "syngas": {c: float(syn.loc[0, c]) for c in SYNGAS_FEATURES},
        "objective": float(J.loc[0]),
        "term_weighted": {k: float(WEIGHTS[k] * terms[k].loc[0]) for k in terms if k != "move"},
    }


def comp_summary(biooil):
    return {c: round(float(biooil[c]), 2) for c in TARGET_FEATURES}


def main():
    df = add_h2_co_ratio(pd.read_csv(DATA_PATH))
    surrogate = ForwardSurrogate.load()
    ids = representative_biooils(df)
    bid = ids["balanced"]
    biooil0 = df[df["BiooilID"] == bid].iloc[0][TARGET_FEATURES]

    opt = MultiObjectiveOptimizer(surrogate, TARGET, weights=WEIGHTS)

    # ADIM 2: bozucu oncesi optimum
    res0 = opt.optimize(biooil0)
    cond0 = res0["conditions"]

    scenarios = {}
    for label, scale in [("standart_8puan", 1.0), ("buyutulmus_24puan", 3.0)]:
        biooil_d = disturb(biooil0, scale)
        # ADIM 3: bozucu sonrasi, ESKI optimum kosulda olculen sapma
        at_old = eval_at(surrogate, biooil_d, cond0, TARGET)
        # ADIM 4: yeni kompozisyonla yeniden optimize
        res1 = opt.optimize(biooil_d)
        cond1 = res1["conditions"]
        moved = any(abs(cond1[c] - cond0[c]) > 1e-6 for c in PROCESS_FEATURES)
        scenarios[label] = {
            "disturbed_composition": comp_summary(biooil_d),
            "step3_at_old_optimum": {
                "H2_CO_Ratio": round(at_old["H2_CO_Ratio"], 4),
                "objective": round(at_old["objective"], 4),
                "deviation_from_target": round(abs(at_old["H2_CO_Ratio"] - TARGET), 4),
            },
            "step4_new_optimum": {
                "conditions": cond1,
                "H2_CO_Ratio": round(res1["H2_CO_Ratio"], 4),
                "objective": round(res1["objective"], 4),
                "deviation_from_target": round(abs(res1["H2_CO_Ratio"] - TARGET), 4),
            },
            "optimum_moved": moved,
            "delta_H2CO_old_vs_new_optimum": round(res1["H2_CO_Ratio"] - res0["H2_CO_Ratio"], 4),
        }

    result = {
        "step1_objective": {"weights": WEIGHTS, "target_h2_co": TARGET,
                            "form": "J = 4*(H2/CO sapma)^2 + 3*(H2 acigi) + 2*CH4 + 1*CO2 + 1.5*enerji + 1.5*koklasma"},
        "biooil": {"name": "balanced", "BiooilID": int(bid), "composition": comp_summary(biooil0)},
        "step2_optimum_before": {
            "conditions": cond0,
            "H2_CO_Ratio": round(res0["H2_CO_Ratio"], 4),
            "syngas": {c: round(res0["syngas"][c], 3) for c in SYNGAS_FEATURES},
            "objective": round(res0["objective"], 4),
            "term_weighted": {k: round(v, 3) for k, v in res0["term_weighted"].items() if k != "move"},
            "deviation_from_target": round(abs(res0["H2_CO_Ratio"] - TARGET), 4),
        },
        "step3_4_disturbance_scenarios": scenarios,
    }
    out = Path(__file__).resolve().parent / "TIK5_CASE_STUDY_4STEP_RESULTS.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("YAZILDI:", out)


if __name__ == "__main__":
    main()
