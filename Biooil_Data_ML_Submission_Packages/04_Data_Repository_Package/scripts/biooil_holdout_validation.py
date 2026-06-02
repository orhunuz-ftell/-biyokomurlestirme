"""BiooilID-based validation for the reverse prediction problem."""

import json

import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import GroupShuffleSplit
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from common import DATA_PATH, INPUT_FEATURES, METRICS_DIR, TARGET_FEATURES, ensure_dirs


def evaluate_biooil_id_holdout(test_size=0.2, random_state=42):
    """Evaluate reverse prediction on fully unseen BiooilID groups.

    This uses an ExtraTrees multi-output model as a fast holdout audit. It is not
    intended to replace the trained MLP; it checks whether the inverse mapping
    generalizes when complete bio-oil identities are held out.
    """
    ensure_dirs()
    df = pd.read_csv(DATA_PATH).dropna(subset=INPUT_FEATURES + TARGET_FEATURES + ["BiooilID"])
    splitter = GroupShuffleSplit(n_splits=1, test_size=test_size, random_state=random_state)
    train_idx, test_idx = next(splitter.split(df, groups=df["BiooilID"]))
    train_df = df.iloc[train_idx]
    test_df = df.iloc[test_idx]

    model = Pipeline(
        steps=[
            ("scale", StandardScaler()),
            (
                "model",
                ExtraTreesRegressor(
                    n_estimators=600,
                    random_state=random_state,
                    min_samples_leaf=1,
                    n_jobs=-1,
                ),
            ),
        ]
    )
    model.fit(train_df[INPUT_FEATURES], train_df[TARGET_FEATURES])
    pred = model.predict(test_df[INPUT_FEATURES])

    metrics = {
        "train_biooil_ids": sorted(train_df["BiooilID"].astype(int).unique().tolist()),
        "test_biooil_ids": sorted(test_df["BiooilID"].astype(int).unique().tolist()),
        "train_samples": int(len(train_df)),
        "test_samples": int(len(test_df)),
        "components": {},
    }

    for idx, col in enumerate(TARGET_FEATURES):
        metrics["components"][col] = {
            "R2": float(r2_score(test_df[col], pred[:, idx])),
            "RMSE": float(np.sqrt(mean_squared_error(test_df[col], pred[:, idx]))),
            "MAE": float(mean_absolute_error(test_df[col], pred[:, idx])),
        }

    metrics["average"] = {
        "R2": float(np.mean([m["R2"] for m in metrics["components"].values()])),
        "RMSE": float(np.mean([m["RMSE"] for m in metrics["components"].values()])),
        "MAE": float(np.mean([m["MAE"] for m in metrics["components"].values()])),
    }

    out_path = METRICS_DIR / "biooil_id_holdout_metrics.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    return metrics


if __name__ == "__main__":
    print(json.dumps(evaluate_biooil_id_holdout(), indent=2))
