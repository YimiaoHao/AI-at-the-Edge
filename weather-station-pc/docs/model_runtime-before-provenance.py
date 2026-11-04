
"""Small JSON-based Ridge model for edge inference."""

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
            for values in (
                self.coefficients,
                self.means,
                self.scales,
            )
        ):
            raise ValueError("Model dimensions do not match")

    def infer(self, row, features):
        """Predict only when the reading and features are usable."""

        if not row.get("valid") or features is None:
            return {
                "prediction_c": None,
                "why": "No valid five-reading feature window."
            }

        if len(features) != len(self.coefficients):
            return {
                "prediction_c": None,
                "why": "Feature count does not match the model."
            }

        if not all(
            isinstance(value, (int, float)) and math.isfinite(value)
            for value in features
        ):
            return {
                "prediction_c": None,
                "why": "Non-finite feature value."
            }

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
            return {
                "prediction_c": None,
                "why": "Prediction is not finite."
            }

        return {
            "prediction_c": float(prediction),
            "why": "Ridge model prediction using five recent readings."
        }
