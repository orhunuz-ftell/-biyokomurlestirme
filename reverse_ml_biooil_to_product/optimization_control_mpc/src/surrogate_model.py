"""Forward surrogate model for fast MPC/optimization simulations."""

import json

import joblib
import numpy as np
import pandas as pd
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.multioutput import MultiOutputRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from common import (
    DATA_PATH,
    MODELS_DIR,
    METRICS_DIR,
    SURROGATE_INPUT_FEATURES,
    SURROGATE_OUTPUT_FEATURES,
    ensure_dirs,
)


def add_h2_co_ratio(df):
    """Ensure H2/CO ratio exists and is finite."""
    df = df.copy()
    if "H2_CO_Ratio" not in df.columns:
        df["H2_CO_Ratio"] = df["H2_molpercent"] / df["CO_molpercent"].replace(0, np.nan)
    df["H2_CO_Ratio"] = df["H2_CO_Ratio"].replace([np.inf, -np.inf], np.nan)
    return df.dropna(subset=SURROGATE_INPUT_FEATURES + SURROGATE_OUTPUT_FEATURES)


class ForwardSurrogate:
    """Predict syngas composition from bio-oil composition and T/P/S-C."""

    def __init__(self, model=None):
        self.model = model

    @staticmethod
    def build_model(random_state=42):
        base = ExtraTreesRegressor(
            n_estimators=200,
            max_depth=None,
            min_samples_leaf=1,
            random_state=random_state,
            n_jobs=-1,
        )
        return Pipeline(
            steps=[
                ("scale", StandardScaler()),
                ("model", MultiOutputRegressor(base, n_jobs=-1)),
            ]
        )

    def fit(self, df):
        self.model = self.build_model()
        self.model.fit(df[SURROGATE_INPUT_FEATURES], df[SURROGATE_OUTPUT_FEATURES])
        return self

    def predict(self, biooil_composition, conditions):
        """Predict syngas for one bio-oil composition and condition dict."""
        row = {}
        row.update({col: float(biooil_composition[col]) for col in SURROGATE_INPUT_FEATURES[:6]})
        row.update(conditions)
        x = pd.DataFrame([row], columns=SURROGATE_INPUT_FEATURES)
        y = self.model.predict(x)
        pred = pd.Series(y[0], index=SURROGATE_OUTPUT_FEATURES)
        pred[["H2_molpercent", "CO_molpercent", "CO2_molpercent", "CH4_molpercent", "H2O_molpercent"]] = (
            pred[["H2_molpercent", "CO_molpercent", "CO2_molpercent", "CH4_molpercent", "H2O_molpercent"]]
            .clip(lower=0.0)
        )
        if pred["CO_molpercent"] > 1e-9:
            pred["H2_CO_Ratio"] = pred["H2_molpercent"] / pred["CO_molpercent"]
        return pred

    def predict_many(self, biooil_composition, conditions_df):
        """Vectorized syngas prediction for many T/P/S-C combinations."""
        rows = pd.DataFrame(
            {
                col: float(biooil_composition[col])
                for col in SURROGATE_INPUT_FEATURES[:6]
            },
            index=conditions_df.index,
        )
        rows = pd.concat([rows, conditions_df.reset_index(drop=True)], axis=1)
        y = self.model.predict(rows[SURROGATE_INPUT_FEATURES])
        pred = pd.DataFrame(y, columns=SURROGATE_OUTPUT_FEATURES)
        syngas_cols = [
            "H2_molpercent",
            "CO_molpercent",
            "CO2_molpercent",
            "CH4_molpercent",
            "H2O_molpercent",
        ]
        pred[syngas_cols] = pred[syngas_cols].clip(lower=0.0)
        pred["H2_CO_Ratio"] = pred["H2_molpercent"] / pred["CO_molpercent"].replace(0, np.nan)
        return pred

    def save(self, path=MODELS_DIR / "forward_surrogate.joblib"):
        path.parent.mkdir(parents=True, exist_ok=True)
        joblib.dump(self.model, path)

    @classmethod
    def load(cls, path=MODELS_DIR / "forward_surrogate.joblib"):
        return cls(joblib.load(path))


def train_and_evaluate():
    """Train surrogate and save metrics/model."""
    ensure_dirs()
    df = add_h2_co_ratio(pd.read_csv(DATA_PATH))
    train_df, test_df = train_test_split(df, test_size=0.2, random_state=42)

    surrogate = ForwardSurrogate().fit(train_df)
    pred = surrogate.model.predict(test_df[SURROGATE_INPUT_FEATURES])
    y_true = test_df[SURROGATE_OUTPUT_FEATURES]

    metrics = {}
    for idx, col in enumerate(SURROGATE_OUTPUT_FEATURES):
        metrics[col] = {
            "R2": float(r2_score(y_true[col], pred[:, idx])),
            "RMSE": float(np.sqrt(mean_squared_error(y_true[col], pred[:, idx]))),
            "MAE": float(mean_absolute_error(y_true[col], pred[:, idx])),
        }
    metrics["average"] = {
        "R2": float(np.mean([m["R2"] for m in metrics.values()])),
        "RMSE": float(np.mean([m["RMSE"] for m in metrics.values()])),
        "MAE": float(np.mean([m["MAE"] for m in metrics.values()])),
    }

    surrogate.save()
    with open(METRICS_DIR / "forward_surrogate_metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
    return surrogate, metrics


if __name__ == "__main__":
    _, result = train_and_evaluate()
    print(json.dumps(result, indent=2))
