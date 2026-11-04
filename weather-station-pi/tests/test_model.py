
"""Week 5 tests: portable model loading and safe abstention."""

import unittest

from model_runtime import Model


MODEL_PATH = "models/temperature_model.json"


class ModelTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.model = Model(MODEL_PATH)

    def make_row(self, valid=True, source="sense_hat"):
        return {
            "valid": valid,
            "source": source,
            "station_id": "station01",
            "sample_interval_s": 5,
            "temperature_c": 29.5,
        }

    def features(self):
        return [29.5, 30.0, 1041.0, 29.4, 30.0, 0.2]

    def test_model_loads(self):
        self.assertEqual(
            self.model.model["model_type"],
            "ridge_regression"
        )

    def test_valid_observation_predicts(self):
        result = self.model.infer(
            self.make_row(),
            self.features()
        )
        self.assertIsInstance(result["prediction_c"], float)

    def test_simulated_source_rejected(self):
        result = self.model.infer(
            self.make_row(source="simulated"),
            self.features()
        )
        self.assertIsNone(result["prediction_c"])

    def test_invalid_observation_rejected(self):
        result = self.model.infer(
            self.make_row(valid=False),
            self.features()
        )
        self.assertIsNone(result["prediction_c"])

    def test_missing_window_rejected(self):
        result = self.model.infer(
            self.make_row(),
            None
        )
        self.assertIsNone(result["prediction_c"])

    def test_wrong_feature_count_rejected(self):
        result = self.model.infer(
            self.make_row(),
            [29.5, 30.0]
        )
        self.assertIsNone(result["prediction_c"])

    def test_wrong_station_rejected(self):
        row = self.make_row()
        row["station_id"] = "station02"

        result = self.model.infer(row, self.features())
        self.assertIsNone(result["prediction_c"])


if __name__ == "__main__":
    unittest.main()
