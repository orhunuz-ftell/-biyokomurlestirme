"""TIK-5 agirlik taramasi — her amac agirligini degistirip optimumun kaymasini olcer.

Ayni amac fonksiyonu (run_multiobjective.MultiObjectiveOptimizer) kullanilir.
Model yeniden EGITILMEZ; kayitli surrogate yuklenir. Statik (soft-sensor gerekmez).
"""

import json
import sys
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parent))
from run_multiobjective import (  # noqa: E402
    MultiObjectiveOptimizer, DEFAULT_WEIGHTS, representative_biooils,
)
from surrogate_model import ForwardSurrogate, add_h2_co_ratio, DATA_PATH  # noqa: E402
from common import TARGET_FEATURES  # noqa: E402

TARGET = 2.5


def opt_summary(res):
    c = res["conditions"]
    return {
        "T": c["Reformer_Temperature_C"], "P": c["Reformer_Pressure_bar"], "SC": c["Steam_to_Carbon_Ratio"],
        "H2_CO": round(res["H2_CO_Ratio"], 3),
        "H2": round(res["syngas"]["H2_molpercent"], 2),
        "CO2": round(res["syngas"]["CO2_molpercent"], 2),
        "CH4": round(res["syngas"]["CH4_molpercent"], 3),
        "objective": round(res["objective"], 3),
        "term_weighted": {k: round(v, 3) for k, v in res["term_weighted"].items() if k != "move"},
    }


def single_weight_sweep(surrogate, biooil):
    """Her terimi tek tek temel degerinin {0, .5, 1, 2, 4} kati yaparak tarar."""
    out = {}
    for key in ["ratio", "h2", "ch4", "co2", "energy", "coke"]:
        base = DEFAULT_WEIGHTS[key]
        levels = []
        for mult in [0.0, 0.5, 1.0, 2.0, 4.0]:
            w = dict(DEFAULT_WEIGHTS)
            w[key] = base * mult
            res = MultiObjectiveOptimizer(surrogate, TARGET, weights=w).optimize(biooil)
            levels.append({"multiplier": mult, "weight_value": round(base * mult, 3),
                           **opt_summary(res)})
        out[key] = levels
    return out


def named_regimes(surrogate, biooil):
    """Sunum icin adlandirilmis rejimler."""
    regimes = {
        "sadece_oran (tek-amacli)": {"ratio": 8.0, "h2": 0, "ch4": 0, "co2": 0, "energy": 0, "coke": 0},
        "dengeli (varsayilan)": dict(DEFAULT_WEIGHTS),
        "verim-baskin": {"ratio": 4.0, "h2": 8.0, "ch4": 6.0, "co2": 1.0, "energy": 0.5, "coke": 0.5},
        "enerji-baskin": {"ratio": 4.0, "h2": 1.0, "ch4": 1.0, "co2": 1.0, "energy": 6.0, "coke": 1.5},
        "koklasma-baskin": {"ratio": 4.0, "h2": 2.0, "ch4": 2.0, "co2": 1.0, "energy": 1.5, "coke": 6.0},
        "cevre-baskin (CO2)": {"ratio": 4.0, "h2": 2.0, "ch4": 2.0, "co2": 6.0, "energy": 1.5, "coke": 1.5},
    }
    return {name: opt_summary(MultiObjectiveOptimizer(surrogate, TARGET, weights=w).optimize(biooil))
            for name, w in regimes.items()}


def main():
    df = add_h2_co_ratio(pd.read_csv(DATA_PATH))
    surrogate = ForwardSurrogate.load()
    ids = representative_biooils(df)
    biooil = df[df["BiooilID"] == ids["balanced"]].iloc[0][TARGET_FEATURES]

    result = {
        "biooil": "balanced", "BiooilID": ids["balanced"], "target_h2_co": TARGET,
        "base_weights": DEFAULT_WEIGHTS,
        "single_weight_sweep": single_weight_sweep(surrogate, biooil),
        "named_regimes": named_regimes(surrogate, biooil),
    }
    out = Path(__file__).resolve().parent / "TIK5_WEIGHT_SWEEP_RESULTS.json"
    out.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print("YAZILDI:", out)


if __name__ == "__main__":
    main()
