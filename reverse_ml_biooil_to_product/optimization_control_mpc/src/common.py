"""Shared constants and path helpers for optimization/MPC work."""

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[2]
MPC_ROOT = Path(__file__).resolve().parents[1]
REVERSE_ML_ROOT = PROJECT_ROOT / "ml_reverse_prediction"

DATA_PATH = REVERSE_ML_ROOT / "data" / "processed" / "reformer_data_clean.csv"
DL_MODEL_DIR = REVERSE_ML_ROOT / "models" / "deep_learning"

RESULTS_DIR = MPC_ROOT / "results"
MODELS_DIR = MPC_ROOT / "models"
FIGURES_DIR = RESULTS_DIR / "figures"
TABLES_DIR = RESULTS_DIR / "tables"
METRICS_DIR = RESULTS_DIR / "metrics"

INPUT_FEATURES = [
    "Reformer_Temperature_C",
    "Reformer_Pressure_bar",
    "Steam_to_Carbon_Ratio",
    "H2_molpercent",
    "CO_molpercent",
    "CO2_molpercent",
    "CH4_molpercent",
    "H2O_molpercent",
]

TARGET_FEATURES = [
    "Biooil_Aromatics_pct",
    "Biooil_Acids_pct",
    "Biooil_Alcohols_pct",
    "Biooil_Furans_pct",
    "Biooil_Phenols_pct",
    "Biooil_Aldehydes_Ketones_pct",
]

PROCESS_FEATURES = [
    "Reformer_Temperature_C",
    "Reformer_Pressure_bar",
    "Steam_to_Carbon_Ratio",
]

SYNGAS_FEATURES = [
    "H2_molpercent",
    "CO_molpercent",
    "CO2_molpercent",
    "CH4_molpercent",
    "H2O_molpercent",
]

SURROGATE_INPUT_FEATURES = TARGET_FEATURES + PROCESS_FEATURES
SURROGATE_OUTPUT_FEATURES = SYNGAS_FEATURES + ["H2_CO_Ratio"]

BOUNDS = {
    "Reformer_Temperature_C": (650.0, 850.0),
    "Reformer_Pressure_bar": (5.0, 30.0),
    "Steam_to_Carbon_Ratio": (2.0, 6.0),
}


def ensure_dirs():
    """Create output directories used by scripts."""
    for path in [RESULTS_DIR, MODELS_DIR, FIGURES_DIR, TABLES_DIR, METRICS_DIR]:
        path.mkdir(parents=True, exist_ok=True)
