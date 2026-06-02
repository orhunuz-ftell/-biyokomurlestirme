"""Static process optimization using the forward surrogate model."""

import pandas as pd

from common import BOUNDS, PROCESS_FEATURES


def energy_cost(temperature_c, pressure_bar, sc_ratio):
    """Dimensionless energy/operation cost proxy."""
    t_norm = (temperature_c - 650.0) / 200.0
    p_norm = (pressure_bar - 5.0) / 25.0
    sc_norm = (sc_ratio - 2.0) / 4.0
    return 0.65 * t_norm + 0.20 * sc_norm + 0.15 * p_norm


class ProcessOptimizer:
    """Optimize T, P, and S/C for a fixed bio-oil composition."""

    def __init__(
        self,
        surrogate,
        target_h2_co=2.0,
        min_h2=25.0,
        max_co2=16.0,
        weights=None,
    ):
        self.surrogate = surrogate
        self.target_h2_co = target_h2_co
        self.min_h2 = min_h2
        self.max_co2 = max_co2
        self.weights = weights or {
            "energy": 1.0,
            "ratio": 8.0,
            "h2_shortfall": 2.5,
            "co2_excess": 0.8,
            "move": 0.0,
        }

    def _candidate_grid(self):
        rows = []
        for t in [650, 675, 700, 725, 750, 775, 800, 825, 850]:
            for p in [5, 10, 15, 20, 25, 30]:
                for sc in [2.0, 3.0, 4.0, 5.0, 6.0]:
                    rows.append(
                        {
                            "Reformer_Temperature_C": float(t),
                            "Reformer_Pressure_bar": float(p),
                            "Steam_to_Carbon_Ratio": float(sc),
                        }
                    )
        return pd.DataFrame(rows)

    def optimize(self, biooil, previous_conditions=None, seed=42, maxiter=25):
        candidates = self._candidate_grid()
        syngas = self.surrogate.predict_many(biooil, candidates)

        ratio_penalty = ((syngas["H2_CO_Ratio"] - self.target_h2_co) / self.target_h2_co) ** 2
        h2_shortfall = ((self.min_h2 - syngas["H2_molpercent"]).clip(lower=0.0) / self.min_h2) ** 2
        co2_excess = ((syngas["CO2_molpercent"] - self.max_co2).clip(lower=0.0) / self.max_co2) ** 2
        cost = candidates.apply(
            lambda row: energy_cost(
                row["Reformer_Temperature_C"],
                row["Reformer_Pressure_bar"],
                row["Steam_to_Carbon_Ratio"],
            ),
            axis=1,
        )

        move_penalty = 0.0
        if previous_conditions is not None:
            move_penalty = (
                ((candidates["Reformer_Temperature_C"] - previous_conditions["Reformer_Temperature_C"]) / 200.0) ** 2
                + ((candidates["Reformer_Pressure_bar"] - previous_conditions["Reformer_Pressure_bar"]) / 25.0) ** 2
                + ((candidates["Steam_to_Carbon_Ratio"] - previous_conditions["Steam_to_Carbon_Ratio"]) / 4.0) ** 2
            ) / 3.0

        objective = (
            self.weights["energy"] * cost
            + self.weights["ratio"] * ratio_penalty
            + self.weights["h2_shortfall"] * h2_shortfall
            + self.weights["co2_excess"] * co2_excess
            + self.weights["move"] * move_penalty
        )
        best_idx = objective.idxmin()
        t = candidates.loc[best_idx, "Reformer_Temperature_C"]
        p = candidates.loc[best_idx, "Reformer_Pressure_bar"]
        sc = candidates.loc[best_idx, "Steam_to_Carbon_Ratio"]
        conditions = {
            "Reformer_Temperature_C": float(t),
            "Reformer_Pressure_bar": float(p),
            "Steam_to_Carbon_Ratio": float(sc),
        }
        pred = syngas.loc[best_idx]
        row = {
            **conditions,
            "objective": float(objective.loc[best_idx]),
            "energy_cost": float(energy_cost(t, p, sc)),
            "target_h2_co": float(self.target_h2_co),
            **{k: float(v) for k, v in pred.to_dict().items()},
        }
        return pd.Series(row)
