
"""Portable Ridge inference with provenance checks and safe abstention."""

import json
import math
from pathlib import Path

from features import FEATURE_NAMES


class Model:
    def __init__(self, path):
        with open(Path(path), "r", encoding="utf-8") as file:
            self.model = json.load(file)

        self.feature_names = self.model["feature_names"]
        self.coefficients = self.model["coefficients"]
        self.intercept = self.model["intercept"]
        self.means = self.model["means"]
        self.scales = self.model["scales"]

        if self.feature_names != list(FEATURE_NAMES):
            raise ValueError("Model feature names do not match the runtime")

        n = len(FEATURE_NAMES)

        if not all(
            len(values) == n
            for values in (self.coefficients, self.means, self.scales)
        ):
            raise ValueError("Model dimensions do not match")

        if not all(
            math.isfinite(value)
            for value in (
                self.intercept,
                *self.coefficients,
                *self.means,
                *self.scales,
            )
        ) or any(scale <= 0 for scale in self.scales):
            raise ValueError("Model contains invalid coefficients or scales")

        if self.model.get("source") != "sense_hat":
            raise ValueError("Model must be trained on real Sense HAT data")

        if self.model.get("horizon_seconds") != 60:
            raise ValueError("Unsupported prediction horizon")

    def infer(self, row, features):
        """Abstain when the input does not match the model's provenance."""

        baseline = row.get("temperature_c")

        def abstain(reason):
            return {
                "prediction_c": None,
                "why": reason
            }

        if not row.get("valid") or features is None:
            return abstain("No valid five-reading feature window.")

        if row.get("source") != self.model["source"]:
            return abstain("Sensor source does not match training data.")

        if row.get("station_id") != self.model.get("station_id"):
            return abstain("Station ID does not match training data.")

        if row.get("sample_interval_s") != self.model.get(
            "sample_interval_s"
        ):
            return abstain("Sampling interval does not match training data.")

        if len(features) != len(self.coefficients):
            return abstain("Feature count does not match the model.")

        if not all(
            isinstance(value, (int, float)) and math.isfinite(value)
            for value in features
        ):
            return abstain("Invalid feature value.")

        if not isinstance(baseline, (int, float)) or not math.isfinite(
            baseline
        ):
            return abstain("Current temperature is unavailable.")

        scaled = [
            (value - mean) / scale
            for value, mean, scale in zip(
                features, self.means, self.scales
            )
        ]

        prediction = self.intercept + sum(
            weight * value
            for weight, value in zip(self.coefficients, scaled)
        )

        if not math.isfinite(prediction):
            return abstain("Prediction is not finite.")

        return {
            "prediction_c": float(prediction),
            "why": "Ridge forecast for approximately 60 seconds ahead."
        }
