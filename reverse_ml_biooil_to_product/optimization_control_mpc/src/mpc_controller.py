"""Simple receding-horizon MPC scenario driven by the reverse ML soft sensor."""

import numpy as np
import pandas as pd

from common import INPUT_FEATURES, PROCESS_FEATURES, SYNGAS_FEATURES, TARGET_FEATURES
from optimization import ProcessOptimizer


class SimpleMPCController:
    """Estimate bio-oil from syngas and optimize the next operating point."""

    def __init__(self, soft_sensor, surrogate, target_h2_co=2.0):
        self.soft_sensor = soft_sensor
        self.surrogate = surrogate
        self.optimizer = ProcessOptimizer(
            surrogate,
            target_h2_co=target_h2_co,
            weights={
                "energy": 1.0,
                "ratio": 8.0,
                "h2_shortfall": 2.5,
                "co2_excess": 0.8,
                "move": 0.25,
            },
        )

    def run(self, initial_biooil, initial_conditions, steps=10, disturbance_step=5):
        """Run a simulated closed-loop MPC case study."""
        actual_biooil = pd.Series(initial_biooil).copy()
        current_conditions = dict(initial_conditions)
        records = []

        for step in range(steps):
            if step == disturbance_step:
                actual_biooil = actual_biooil.copy()
                actual_biooil["Biooil_Acids_pct"] += 8.0
                actual_biooil["Biooil_Aromatics_pct"] -= 6.0
                actual_biooil["Biooil_Phenols_pct"] -= 2.0
                actual_biooil = actual_biooil.clip(lower=0.0)
                actual_biooil = actual_biooil / actual_biooil.sum() * 100.0

            measured_syngas = self.surrogate.predict(actual_biooil, current_conditions)
            measurement_row = {
                **current_conditions,
                **{col: measured_syngas[col] for col in SYNGAS_FEATURES},
            }
            estimated_biooil = self.soft_sensor.predict(pd.DataFrame([measurement_row]))[TARGET_FEATURES].iloc[0]

            optimum = self.optimizer.optimize(
                estimated_biooil,
                previous_conditions=current_conditions,
                seed=100 + step,
                maxiter=18,
            )
            next_conditions = {col: float(optimum[col]) for col in PROCESS_FEATURES}

            records.append(
                {
                    "step": step,
                    **{f"actual_{col}": float(actual_biooil[col]) for col in TARGET_FEATURES},
                    **{f"estimated_{col}": float(estimated_biooil[col]) for col in TARGET_FEATURES},
                    **{f"measured_{col}": float(measured_syngas[col]) for col in SYNGAS_FEATURES},
                    "measured_H2_CO_Ratio": float(measured_syngas["H2_CO_Ratio"]),
                    **{f"applied_{col}": float(current_conditions[col]) for col in PROCESS_FEATURES},
                    **{f"next_{col}": float(next_conditions[col]) for col in PROCESS_FEATURES},
                    "next_predicted_H2_CO_Ratio": float(optimum["H2_CO_Ratio"]),
                    "next_predicted_H2_molpercent": float(optimum["H2_molpercent"]),
                    "next_predicted_CO2_molpercent": float(optimum["CO2_molpercent"]),
                    "next_energy_cost": float(optimum["energy_cost"]),
                    "objective": float(optimum["objective"]),
                }
            )
            current_conditions = next_conditions

        return pd.DataFrame(records)
