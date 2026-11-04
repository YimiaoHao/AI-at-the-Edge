# Week 7 – Data Retention and MQTT Cleanup Evidence

## 1. Retention Test

**Command used:**

`python inspect_data.py --config config_sim.json --purge`

**Observed results:**

- Removed old database rows: 0
- Remaining simulated observations: 28
- Data source: `simulated`

**Interpretation:**

The cleanup command completed successfully without deleting recent simulated observations.

Since no expired rows were present, this particular run does not independently demonstrate the removal of expired data. The SQLite purge behaviour was also covered by an earlier unit test.

## 2. MQTT Retained Message Cleanup

**Preparation:**

I stopped the station before cleanup and temporarily started Mosquitto.

**Commands used:**

```bash
sudo systemctl start mosquitto
python clear_retained.py
```

I entered `station01` to confirm that only my station's retained messages should be cleared.

**Observed result:**

`Broker acknowledged empty retained values. Verify with a new subscription; remove archives and exports separately.`

## 3. Verification

I checked both topics using new subscriptions:

```bash
timeout 5 mosquitto_sub -h localhost -t "weather/station01/telemetry" -v
timeout 5 mosquitto_sub -h localhost -t "weather/station01/status" -v
```

Neither subscription displayed a retained message during the test.

I then ran:

```bash
sudo systemctl stop mosquitto
sudo systemctl disable mosquitto
sudo systemctl is-active mosquitto
```

The final service state was:

`inactive`

## 4. What This Evidence Establishes

The tests support that the two named retained MQTT topics were cleared and that the classroom broker was subsequently stopped.

The retention test also shows that recent simulated observations were preserved.

However, clearing retained MQTT messages does not remove copies from SQLite databases, CSV exports, training datasets or backups.

These tests do not demonstrate secure forensic erasure of stored data.

## 5. Reflection

This exercise showed me why a deletion claim must identify the exact storage location and be supported by observable results.

I also learned that retaining data for a limited period requires both a defined policy and a way to verify that cleanup actually happens.
