
"""Week 6: run one station process. Ctrl+C stops it safely."""

import argparse
import fcntl
import json
import time
import uuid

from common import ROOT, load_config, observation, project_path
from sensors import Sensor
from storage import Store
from features import FeatureWindow
from context import ContextPolicy
from timing import measure, append_runtime
from matrix import Matrix


def main():
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument("--config", default="config.json")
    parser.add_argument("--simulate", action="store_true")
    parser.add_argument("--samples", type=int, default=0)
    parser.add_argument("--fault-every", type=int, default=0)
    parser.add_argument("--no-mqtt", action="store_true")
    parser.add_argument(
        "--model",
        default=None,
        help="Path to the exported temperature model JSON"
    )

    args = parser.parse_args()

    if args.samples < 0 or args.fault_every < 0 or (
        args.fault_every and not args.simulate
    ):
        raise SystemExit(
            "Counts cannot be negative; --fault-every requires --simulate."
        )

    config = load_config(args.config)
    database = project_path(config["database"])

    if args.simulate and "sim" not in database.stem:
        raise SystemExit(
            "Simulation needs a database name containing 'sim'."
        )

    store = Store(database)

    lockfile = ROOT / "data" / "station.lock"
    lockfile.parent.mkdir(parents=True, exist_ok=True)
    lock = lockfile.open("w")

    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        lock.close()
        raise SystemExit(
            "Another station.py is running. Stop it first."
        )

    sensor = None
    publisher = None

    try:
        sensor = Sensor(simulated=args.simulate)

        # Week 6: only the station process owns the Sense HAT display.
        display = Matrix(sensor)

        run_id = uuid.uuid4().hex[:12]
        sequence = 0

        if not args.no_mqtt:
            from mqtt_link import Publisher
            publisher = Publisher(config)

        window = FeatureWindow()
        policy = ContextPolicy()

        model = None

        if args.model:
            try:
                from model_runtime import Model
                model = Model(project_path(args.model))
                print("Ridge model loaded. Forecasts run in shadow mode.")
            except (OSError, ValueError, KeyError, TypeError) as exc:
                print(
                    "Model unavailable; observed-data rules still work:",
                    exc
                )

        next_sample = time.monotonic()
        last_purge = 0

        try:
            while True:
                now = time.monotonic()

                if now - last_purge > 3600:
                    store.purge(config["retention_days"])
                    last_purge = now

                if now >= next_sample:
                    values, error = sensor.read(
                        config["temperature_offset_c"]
                    )

                    sequence += 1

                    if (
                        args.fault_every
                        and sequence % args.fault_every == 0
                    ):
                        values["temperature_c"] = None

                    row = observation(
                        config,
                        values,
                        run_id,
                        sequence,
                        time.time(),
                        sensor.source,
                        error
                    )

                    row["mqtt_state"] = (
                        "connected"
                        if publisher and publisher.client.is_connected()
                        else "local_only_or_offline"
                    )

                    features = window.push(row)
                    row["context"] = policy.update(row, features)

                    row["forecast"] = {
                        "prediction_c": None,
                        "why": (
                            "No usable model loaded; "
                            "persistence baseline only."
                        )
                    }

                    if model is not None:
                        try:
                            forecast, metrics = measure(
                                "ridge_inference",
                                model.infer,
                                row,
                                features
                            )

                            row["forecast"] = forecast

                            if forecast["prediction_c"] is not None:
                                append_runtime(
                                    project_path("data/runtime.csv"),
                                    row["observed_at"],
                                    metrics
                                )

                        except (ValueError, TypeError, ArithmeticError) as exc:
                            row["forecast"] = {
                                "prediction_c": None,
                                "why": f"Model inference unavailable: {exc}"
                            }

                    row["prediction_c"] = row["forecast"]["prediction_c"]

                    # Week 6: apply the display state and record acknowledgement.
                    display.service(row, store)

                    # Always save locally before network transmission.
                    store.add(row)

                    if publisher:
                        publisher.publish(row)

                    print(json.dumps(row, allow_nan=False))

                    if args.samples and sequence >= args.samples:
                        break

                    next_sample += config["sample_interval_s"]

                    # Service display controls between sensor readings.
                    display.service(row, store)

                    if next_sample < time.monotonic():
                        next_sample = (
                            time.monotonic()
                            + config["sample_interval_s"]
                        )

                time.sleep(0.5)

        except KeyboardInterrupt:
            print("Station stopped safely.")

    finally:
        try:
            if sensor is not None:
                sensor.close()
        finally:
            if publisher:
                publisher.close()
            lock.close()


if __name__ == "__main__":
    main()
