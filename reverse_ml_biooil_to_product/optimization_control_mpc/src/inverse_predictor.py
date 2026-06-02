"""Prediction interface for the trained reverse MLP soft sensor."""

import joblib
import numpy as np
import pandas as pd
from tensorflow import keras

from common import DL_MODEL_DIR, INPUT_FEATURES, TARGET_FEATURES


class ReverseMLSoftSensor:
    """Load the trained reverse MLP and predict bio-oil composition."""

    def __init__(self, model_dir=DL_MODEL_DIR, normalize_output=True):
        self.model_dir = model_dir
        self.normalize_output = normalize_output
        self.model = keras.models.load_model(model_dir / "mlp_standard.h5")
        self.scaler_x = joblib.load(model_dir / "scaler_X.pkl")
        self.scaler_y = joblib.load(model_dir / "scaler_y.pkl")

    def predict(self, inputs):
        """Predict bio-oil composition from process conditions and syngas.

        Args:
            inputs: dict, Series, or DataFrame containing INPUT_FEATURES.

        Returns:
            DataFrame with TARGET_FEATURES in wt%.
        """
        if isinstance(inputs, dict):
            frame = pd.DataFrame([inputs])
        elif isinstance(inputs, pd.Series):
            frame = inputs.to_frame().T
        else:
            frame = inputs.copy()

        missing = [col for col in INPUT_FEATURES if col not in frame.columns]
        if missing:
            raise ValueError(f"Missing input columns: {missing}")

        x = frame[INPUT_FEATURES]
        x_scaled = self.scaler_x.transform(x)
        y_scaled = self.model.predict(x_scaled, verbose=0)
        y = self.scaler_y.inverse_transform(y_scaled)
        y = np.clip(y, 0.0, None)

        if self.normalize_output:
            sums = y.sum(axis=1, keepdims=True)
            sums[sums == 0.0] = 1.0
            y = y / sums * 100.0

        return pd.DataFrame(y, columns=TARGET_FEATURES, index=frame.index)
