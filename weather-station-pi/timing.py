
"""Record inference timing with bounded CSV log rotation."""

import csv
import resource
import time
from pathlib import Path


FIELDS = [
    "observed_at",
    "operation",
    "duration_ms",
    "cpu_seconds",
    "max_rss_kb",
]

MAX_LOG_BYTES = 1_000_000


def measure(operation, function, *args, **kwargs):
    """Measure one operation, excluding sensor reads and storage."""
    cpu_before = time.process_time()
    start = time.perf_counter_ns()

    result = function(*args, **kwargs)

    duration_ms = (time.perf_counter_ns() - start) / 1_000_000
    cpu_seconds = time.process_time() - cpu_before
    max_rss_kb = resource.getrusage(
        resource.RUSAGE_SELF
    ).ru_maxrss

    metrics = {
        "operation": operation,
        "duration_ms": round(duration_ms, 6),
        "cpu_seconds": round(cpu_seconds, 6),
        "max_rss_kb": max_rss_kb,
    }

    return result, metrics


def append_runtime(path, observed_at, metrics):
    """Append metrics and keep the runtime CSV from growing forever."""
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)

    if target.exists() and target.stat().st_size >= MAX_LOG_BYTES:
        rotated = target.with_name(
            target.stem + ".previous" + target.suffix
        )

        # Keep one previous log; replace any older rotated copy.
        target.replace(rotated)

    needs_header = (
        not target.exists()
        or target.stat().st_size == 0
    )

    with target.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=FIELDS)

        if needs_header:
            writer.writeheader()

        writer.writerow({
            "observed_at": observed_at,
            **metrics,
        })
