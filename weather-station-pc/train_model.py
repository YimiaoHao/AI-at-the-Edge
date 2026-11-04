
"""Week 5: train and evaluate a 60-second temperature forecast."""

import json
import math
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.preprocessing import StandardScaler

from features import FEATURE_NAMES, WINDOW_SIZE, continuous, feature_vector


ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "data" / "weather.db"
OUTPUT = ROOT / "models"

HORIZON_STEPS = 12
ALPHAS = (0.01, 0.1, 1.0, 10.0, 100.0)
MIN_EXAMPLES = 40


def read_observations():
    """Read real observations in chronological order."""
    with sqlite3.connect(DATABASE) as connection:
        records = connection.execute(
            "SELECT body FROM readings ORDER BY epoch, station, sample"
        ).fetchall()

    rows = [json.loads(record[0]) for record in records]

    return [
        row for row in rows
        if row.get("source") == "sense_hat"
    ]


def make_examples(rows):
    """Build examples without crossing invalid readings or run boundaries."""
    examples = []
    segment = []

    def process_segment(items):
        needed = WINDOW_SIZE + HORIZON_STEPS

        if len(items) < needed:
            return

        for start in range(len(items) - needed + 1):
            window = items[start:start + WINDOW_SIZE]
            target = items[
                start + WINDOW_SIZE - 1 + HORIZON_STEPS
            ]

            features = feature_vector(window)

            examples.append({
                "features": features,
                "target": float(target["temperature_c"]),
                "baseline": float(window[-1]["temperature_c"]),
                "observed_at": window[-1]["observed_at"],
                "target_at": target["observed_at"],
                "run_id": window[-1]["run_id"],
            })

    for row in rows:
        if not row.get("valid"):
            process_segment(segment)
            segment = []
            continue

        if segment and not continuous(segment[-1], row):
            process_segment(segment)
            segment = []

        segment.append(row)

    process_segment(segment)

    return examples


def arrays(examples):
    X = np.asarray(
        [item["features"] for item in examples],
        dtype=float
    )

    y = np.asarray(
        [item["target"] for item in examples],
        dtype=float
    )

    baseline = np.asarray(
        [item["baseline"] for item in examples],
        dtype=float
    )

    return X, y, baseline


def evaluate(actual, predicted):
    return {
        "mae_c": float(mean_absolute_error(actual, predicted)),
        "rmse_c": float(
            math.sqrt(mean_squared_error(actual, predicted))
        )
    }


def main():
    rows = read_observations()

    if len(rows) < 600:
        raise SystemExit(
            f"Not enough real observations: {len(rows)}"
        )

    # Split raw chronological observations BEFORE making windows.
    # This prevents input/target overlap across dataset partitions.
    train_end = int(len(rows) * 0.70)
    validation_end = int(len(rows) * 0.85)

    partitions = {
        "train": rows[:train_end],
        "validation": rows[train_end:validation_end],
        "test": rows[validation_end:],
    }

    examples = {
        name: make_examples(part)
        for name, part in partitions.items()
    }

    counts = {
        name: len(items)
        for name, items in examples.items()
    }

    print("Raw observations:", len(rows))
    print("Raw partition sizes:", {
        name: len(part)
        for name, part in partitions.items()
    })
    print("Usable examples:", counts)

    if any(count < MIN_EXAMPLES for count in counts.values()):
        raise SystemExit(
            "Not enough continuous examples in every partition. "
            "Do not mix future data into training to fix this."
        )

    X_train, y_train, baseline_train = arrays(examples["train"])
    X_val, y_val, baseline_val = arrays(examples["validation"])
    X_test, y_test, baseline_test = arrays(examples["test"])

    # The scaler is fitted on TRAINING DATA ONLY.
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_val_scaled = scaler.transform(X_val)

    candidates = []

    for alpha in ALPHAS:
        model = Ridge(alpha=alpha)
        model.fit(X_train_scaled, y_train)

        prediction = model.predict(X_val_scaled)
        score = evaluate(y_val, prediction)

        candidates.append({
            "alpha": alpha,
            "validation_mae_c": score["mae_c"],
        })

    selected = min(
        candidates,
        key=lambda item: item["validation_mae_c"]
    )

    print("Selected Ridge alpha:", selected["alpha"])

    # Refit with training + validation after selecting alpha.
    # The test partition stays untouched until final evaluation.
    X_development = np.vstack([X_train, X_val])
    y_development = np.concatenate([y_train, y_val])

    final_scaler = StandardScaler()
    X_development_scaled = final_scaler.fit_transform(
        X_development
    )

    final_model = Ridge(alpha=selected["alpha"])
    final_model.fit(X_development_scaled, y_development)

    X_test_scaled = final_scaler.transform(X_test)
    predictions = final_model.predict(X_test_scaled)

    test_baseline = evaluate(y_test, baseline_test)
    test_ridge = evaluate(y_test, predictions)
    validation_baseline = evaluate(y_val, baseline_val)

    print("\nValidation baseline:", validation_baseline)
    print("Test baseline:", test_baseline)
    print("Test Ridge:", test_ridge)

    OUTPUT.mkdir(parents=True, exist_ok=True)

    # Export a portable model for pure-Python inference on the Pi.
    # Field names match model_runtime.py.
    model_data = {
        "model_type": "ridge_regression",
        "schema_version": 1,
        "feature_names": list(FEATURE_NAMES),
        "horizon_steps": HORIZON_STEPS,
        "horizon_seconds": 60,
        "sample_interval_s": 5,
        "source": "sense_hat",
        "station_id": "station01",
        "selected_alpha": selected["alpha"],
        "coefficients": [
            float(value) for value in final_model.coef_
        ],
        "intercept": float(final_model.intercept_),
        "means": [
            float(value) for value in final_scaler.mean_
        ],
        "scales": [
            float(value) for value in final_scaler.scale_
        ],
        "training_rows": len(rows),
    }

    report = {
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "objective": "Predict temperature approximately 60 seconds ahead",
        "data_source": "Real Sense HAT observations",
        "raw_observations": len(rows),
        "raw_partition_sizes": {
            name: len(part)
            for name, part in partitions.items()
        },
        "usable_examples": counts,
        "split_method": (
            "Chronological raw-data split before feature and target "
            "construction; no overlapping partition windows"
        ),
        "feature_names": list(FEATURE_NAMES),
        "horizon_steps": HORIZON_STEPS,
        "alpha_candidates": candidates,
        "selected_alpha": selected["alpha"],
        "validation_persistence": validation_baseline,
        "test_persistence": test_baseline,
        "test_ridge": test_ridge,
        "ridge_beats_persistence": (
            test_ridge["mae_c"] < test_baseline["mae_c"]
        ),
        "limitations": [
            "Only one Sense HAT station was used.",
            "The Pi may heat the temperature sensor.",
            "Performance on other dates or devices is untested.",
            "This is an experimental forecast, not a warning service."
        ],
    }

    cases = []

    for item, prediction in zip(examples["test"], predictions):
        cases.append({
            "observed_at": item["observed_at"],
            "target_at": item["target_at"],
            "actual_c": item["target"],
            "baseline_c": item["baseline"],
            "ridge_c": float(prediction),
        })

    paths = {
        "model": OUTPUT / "temperature_model.json",
        "report": OUTPUT / "temperature_model.report.json",
        "cases": OUTPUT / "temperature_model.cases.json",
    }

    outputs = {
        "model": model_data,
        "report": report,
        "cases": cases,
    }

    for name, path in paths.items():
        path.write_text(
            json.dumps(outputs[name], indent=2, allow_nan=False),
            encoding="utf-8"
        )

    print("\nSaved files:")
    for path in paths.values():
        print(" ", path)

    if report["ridge_beats_persistence"]:
        print("\nRidge achieved lower test MAE than persistence.")
    else:
        print(
            "\nPersistence matched or beat Ridge on test MAE. "
            "This is a valid experimental result."
        )


if __name__ == "__main__":
    main()
