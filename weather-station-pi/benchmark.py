
"""Benchmark portable Ridge inference on the Raspberry Pi."""

import argparse
import json
import statistics
import time
from pathlib import Path

from common import load_config, project_path
from features import FEATURE_NAMES
from model_runtime import Model
from timing import measure


def percentile(values, fraction):
    values = sorted(values)
    position = (len(values) - 1) * fraction
    low = int(position)
    high = min(low + 1, len(values) - 1)
    weight = position - low
    return values[low] * (1 - weight) + values[high] * weight


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        default="models/temperature_model.json"
    )
    parser.add_argument("--iterations", type=int, default=1000)
    args = parser.parse_args()

    if args.iterations < 20:
        raise SystemExit("Use at least 20 iterations.")

    config = load_config("config.json")
    model = Model(project_path(args.model))

    # A labelled representative input, not new measured evidence.
    row = {
        "valid": True,
        "source": "sense_hat",
        "station_id": config["station_id"],
        "sample_interval_s": config["sample_interval_s"],
        "temperature_c": 29.5,
    }

    features = [29.5, 30.0, 1041.0, 29.4, 30.0, 0.2]

    if len(features) != len(FEATURE_NAMES):
        raise SystemExit("Feature count mismatch.")

    durations = []
    cpu_times = []
    memory = []

    # Warm up the interpreter before measuring.
    for _ in range(20):
        model.infer(row, features)

    started = time.perf_counter()

    for _ in range(args.iterations):
        forecast, metrics = measure(
            "ridge_inference",
            model.infer,
            row,
            features
        )

        if forecast["prediction_c"] is None:
            raise SystemExit(
                "Model rejected the benchmark input: "
                + forecast["why"]
            )

        durations.append(metrics["duration_ms"])
        cpu_times.append(metrics["cpu_seconds"])
        memory.append(metrics["max_rss_kb"])

    elapsed = time.perf_counter() - started

    result = {
        "iterations": args.iterations,
        "operation": "ridge_inference",
        "median_ms": statistics.median(durations),
        "p95_ms": percentile(durations, 0.95),
        "mean_ms": statistics.mean(durations),
        "mean_cpu_seconds": statistics.mean(cpu_times),
        "peak_process_rss_kb": max(memory),
        "wall_seconds_total": elapsed,
        "note": (
            "Synthetic representative input; inference timing only. "
            "Sensor reads, SQLite and MQTT are not included."
        ),
    }

    print(json.dumps(result, indent=2))

    output = Path("data/benchmark-latest.json")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(
        json.dumps(result, indent=2),
        encoding="utf-8"
    )

    print("Saved:", output)


if __name__ == "__main__":
    main()
