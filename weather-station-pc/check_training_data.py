
"""Check whether real Sense HAT readings can form 60-second training examples."""

import json
import sqlite3
from collections import Counter

from features import FeatureWindow, continuous

DATABASE = "data/weather.db"
HORIZON_STEPS = 12

connection = sqlite3.connect(DATABASE)

try:
    records = connection.execute(
        "SELECT body FROM readings ORDER BY epoch, station, sample"
    ).fetchall()
finally:
    connection.close()

rows = [json.loads(record[0]) for record in records]

sources = Counter(row.get("source") for row in rows)
valid_count = sum(row.get("valid") is True for row in rows)

# Separate runs whenever a timestamp, run or calibration discontinuity occurs.
segments = []
segment = []

for row in rows:
    if row.get("source") != "sense_hat" or not row.get("valid"):
        if segment:
            segments.append(segment)
        segment = []
        continue

    if segment and not continuous(segment[-1], row):
        segments.append(segment)
        segment = []

    segment.append(row)

if segment:
    segments.append(segment)

# Five input observations followed by a target 12 intervals after
# the most recent input observation.
examples_per_segment = [
    max(0, len(segment) - 4 - HORIZON_STEPS)
    for segment in segments
]

total_examples = sum(examples_per_segment)

print("Total database rows:", len(rows))
print("Valid rows:", valid_count)
print("Sources:", dict(sources))
print("Continuous segments:", len(segments))
print("Longest segment:", max(map(len, segments), default=0))
print("Usable 60-second examples:", total_examples)
print("Largest segments:", sorted(map(len, segments), reverse=True)[:10])

if total_examples >= 120:
    print("Initial result: enough examples to investigate chronological splits.")
else:
    print("Initial result: training may need more continuous observations.")
