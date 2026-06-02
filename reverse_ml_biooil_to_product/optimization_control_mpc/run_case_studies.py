"""Run optimization/MPC case studies and save thesis-ready outputs."""

import json
import sys
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

SRC_DIR = Path(__file__).resolve().parent / "src"
sys.path.insert(0, str(SRC_DIR))

from biooil_holdout_validation import evaluate_biooil_id_holdout
from common import (
    DATA_PATH,
    FIGURES_DIR,
    METRICS_DIR,
    PROCESS_FEATURES,
    TABLES_DIR,
    TARGET_FEATURES,
    ensure_dirs,
)
from inverse_predictor import ReverseMLSoftSensor
from mpc_controller import SimpleMPCController
from optimization import ProcessOptimizer, energy_cost
from surrogate_model import ForwardSurrogate, train_and_evaluate


def select_case_biooils(df):
    """Select three representative compositions."""
    grouped = df.groupby("BiooilID")[TARGET_FEATURES].first().reset_index()
    aromatic_id = grouped.sort_values("Biooil_Aromatics_pct", ascending=False).iloc[0]["BiooilID"]
    acid_id = grouped.sort_values("Biooil_Acids_pct", ascending=False).iloc[0]["BiooilID"]
    balanced = grouped.copy()
    balanced["spread"] = grouped[TARGET_FEATURES].std(axis=1)
    balanced_id = balanced.sort_values("spread").iloc[0]["BiooilID"]
    cases = {
        "aromatic_rich": int(aromatic_id),
        "acid_rich": int(acid_id),
        "balanced": int(balanced_id),
    }
    return cases


def run_static_cases(surrogate, df):
    """Optimize three representative bio-oils for H2/CO=2.0 and 2.5."""
    cases = select_case_biooils(df)
    rows = []
    for case_name, biooil_id in cases.items():
        biooil = df[df["BiooilID"] == biooil_id].iloc[0][TARGET_FEATURES]
        baseline_conditions = {
            "Reformer_Temperature_C": 750.0,
            "Reformer_Pressure_bar": 15.0,
            "Steam_to_Carbon_Ratio": 4.0,
        }
        baseline = surrogate.predict(biooil, baseline_conditions)
        for target_ratio in [2.0, 2.5]:
            optimizer = ProcessOptimizer(surrogate, target_h2_co=target_ratio)
            optimum = optimizer.optimize(biooil, seed=42 + int(target_ratio * 10), maxiter=25)
            rows.append(
                {
                    "case": case_name,
                    "BiooilID": biooil_id,
                    "target_h2_co": target_ratio,
                    "baseline_T": baseline_conditions["Reformer_Temperature_C"],
                    "baseline_P": baseline_conditions["Reformer_Pressure_bar"],
                    "baseline_SC": baseline_conditions["Steam_to_Carbon_Ratio"],
                    "baseline_H2_CO_Ratio": baseline["H2_CO_Ratio"],
                    "baseline_H2_molpercent": baseline["H2_molpercent"],
                    "baseline_CO2_molpercent": baseline["CO2_molpercent"],
                    "baseline_energy_cost": energy_cost(750.0, 15.0, 4.0),
                    **optimum.to_dict(),
                }
            )
    result = pd.DataFrame(rows)
    result.to_csv(TABLES_DIR / "static_optimization_cases.csv", index=False)
    return result


def make_figures(static_df, mpc_df):
    """Generate compact figures for reporting."""
    plt.style.use("seaborn-v0_8-whitegrid")

    fig, ax = plt.subplots(figsize=(8, 4.5))
    labels = static_df["case"] + " / " + static_df["target_h2_co"].astype(str)
    x = range(len(static_df))
    ax.plot(x, static_df["baseline_H2_CO_Ratio"], "o--", label="Baseline")
    ax.plot(x, static_df["H2_CO_Ratio"], "s-", label="Optimized")
    ax.plot(x, static_df["target_h2_co"], "k:", label="Target")
    ax.set_xticks(list(x))
    ax.set_xticklabels(labels, rotation=35, ha="right")
    ax.set_ylabel("H2/CO ratio")
    ax.set_title("Static optimization: target H2/CO tracking")
    ax.legend()
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "static_optimization_h2co.png", dpi=200)
    plt.close(fig)

    fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True)
    axes[0].plot(mpc_df["step"], mpc_df["measured_H2_CO_Ratio"], "o-", label="Measured current")
    axes[0].plot(mpc_df["step"], mpc_df["next_predicted_H2_CO_Ratio"], "s-", label="Next predicted")
    axes[0].axhline(2.0, color="black", linestyle=":", label="Target")
    axes[0].set_ylabel("H2/CO")
    axes[0].legend()
    axes[1].plot(mpc_df["step"], mpc_df["next_Reformer_Temperature_C"], label="T (C)")
    axes[1].plot(mpc_df["step"], mpc_df["next_Reformer_Pressure_bar"], label="P (bar)")
    axes[1].plot(mpc_df["step"], mpc_df["next_Steam_to_Carbon_Ratio"], label="S/C")
    axes[1].set_xlabel("MPC step")
    axes[1].set_ylabel("Next control move")
    axes[1].legend()
    fig.suptitle("MPC case study with composition disturbance")
    fig.tight_layout()
    fig.savefig(FIGURES_DIR / "mpc_case_study_timeseries.png", dpi=200)
    plt.close(fig)


def main():
    ensure_dirs()
    print("Training/evaluating forward surrogate...")
    surrogate, surrogate_metrics = train_and_evaluate()

    print("Running BiooilID holdout validation audit...")
    holdout_metrics = evaluate_biooil_id_holdout()

    df = pd.read_csv(DATA_PATH)
    print("Running static optimization cases...")
    static_df = run_static_cases(surrogate, df)

    print("Running MPC scenario...")
    soft_sensor = ReverseMLSoftSensor()
    initial_biooil = df[df["BiooilID"] == select_case_biooils(df)["balanced"]].iloc[0][TARGET_FEATURES]
    initial_conditions = {
        "Reformer_Temperature_C": 750.0,
        "Reformer_Pressure_bar": 15.0,
        "Steam_to_Carbon_Ratio": 4.0,
    }
    mpc = SimpleMPCController(soft_sensor, surrogate, target_h2_co=2.0)
    mpc_df = mpc.run(initial_biooil, initial_conditions, steps=10, disturbance_step=5)
    mpc_df.to_csv(TABLES_DIR / "mpc_case_study.csv", index=False)

    make_figures(static_df, mpc_df)

    summary = {
        "forward_surrogate_average": surrogate_metrics["average"],
        "biooil_id_holdout_average": holdout_metrics["average"],
        "static_cases": static_df[
            [
                "case",
                "BiooilID",
                "target_h2_co",
                "baseline_H2_CO_Ratio",
                "H2_CO_Ratio",
                "energy_cost",
                "Reformer_Temperature_C",
                "Reformer_Pressure_bar",
                "Steam_to_Carbon_Ratio",
            ]
        ].to_dict(orient="records"),
        "mpc_final": mpc_df.tail(1).to_dict(orient="records")[0],
    }
    with open(METRICS_DIR / "case_study_summary.json", "w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
