
"""Tests for the Week 4 feature window and context policy."""

import unittest

from features import FeatureWindow, feature_vector
from context import ContextPolicy, heat_index_c


def make_row(sequence, temperature=25, humidity=60, valid=True, run_id="test-run"):
    return {
        "station_id": "station01",
        "run_id": run_id,
        "source": "simulated",
        "calibration_id": "uncalibrated",
        "temperature_offset_c": 0.0,
        "sample_interval_s": 5,
        "observed_epoch": 1000 + sequence * 5,
        "temperature_c": temperature,
        "humidity_pct": humidity,
        "pressure_hpa": 1013,
        "valid": valid,
    }


class ContextTests(unittest.TestCase):

    def test_five_reading_features(self):
        rows = [
            make_row(i, temperature=20 + i)
            for i in range(5)
        ]
        result = feature_vector(rows)

        self.assertEqual(result[3], 22)
        self.assertEqual(result[5], 4)

    def test_window_needs_five_valid_readings(self):
        window = FeatureWindow()

        for i in range(4):
            self.assertIsNone(window.push(make_row(i)))

        self.assertIsNotNone(window.push(make_row(4)))

    def test_invalid_reading_resets_window(self):
        window = FeatureWindow()

        for i in range(5):
            window.push(make_row(i))

        self.assertIsNone(
            window.push(make_row(5, valid=False))
        )
        self.assertIsNone(window.push(make_row(6)))

    def test_run_change_resets_window(self):
        window = FeatureWindow()

        for i in range(4):
            window.push(make_row(i))

        self.assertIsNone(
            window.push(make_row(4, run_id="new-run"))
        )

    def test_attention_hysteresis(self):
        policy = ContextPolicy()
        row = make_row(4)

        hot = [29, 60, 1013, 28, 60, 3]
        middle = [27, 60, 1013, 27, 60, 0]
        cool = [25, 60, 1013, 25, 60, -2]

        self.assertEqual(
            policy.update(row, hot)["state"], "attention"
        )
        self.assertEqual(
            policy.update(row, middle)["state"], "attention"
        )
        self.assertEqual(
            policy.update(row, cool)["state"], "normal"
        )

    def test_invalid_reading_is_unknown(self):
        policy = ContextPolicy()
        row = make_row(0, valid=False)

        result = policy.update(row, None)
        self.assertEqual(result["state"], "unknown")

    def test_heat_index_domain(self):
        self.assertIsNone(heat_index_c(20, 60))
        self.assertIsNotNone(heat_index_c(30, 70))


if __name__ == "__main__":
    unittest.main()
