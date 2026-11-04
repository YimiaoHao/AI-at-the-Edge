# AI at the Edge – Raspberry Pi Weather Station

## Project Overview

This project is an indoor weather station developed using a Raspberry Pi 4 and Sense HAT for the AI at the Edge module.

The system collects temperature, relative humidity and atmospheric pressure readings approximately every five seconds. It stores observations locally, evaluates environmental conditions, and runs a lightweight machine learning model to predict temperature approximately 60 seconds ahead.

The project also includes MQTT communication, a physical LED status display and a local Flask dashboard.

## System Architecture

```text
Sense HAT
    |
    v
Raspberry Pi – station.py
    |
    +-- SQLite local storage
    |
    +-- Five-reading feature window
    |
    +-- Context rules and LED display
    |
    +-- Ridge temperature forecast
    |
    +-- MQTT publisher (optional)
    |       |
    |       v
    |   Mosquitto broker
    |       |
    |       v
    |   Windows PC receiver
    |
    +-- Flask dashboard (reads local SQLite)
```

## Hardware and Software

- Raspberry Pi 4 with Sense HAT
- Raspberry Pi OS
- Python 3.13
- SQLite for local storage
- Paho MQTT for messaging
- Flask for the dashboard
- Ridge Regression model exported as JSON

The Raspberry Pi uses a lightweight Python inference implementation without requiring Scikit-learn at runtime.

## Environment Setup

From the project directory:

```bash
python3 -m venv --system-site-packages .venv
source .venv/bin/activate
python -m pip install -r requirements-network.txt
python -m pip install -r requirements-web.txt
```

Sense HAT hardware support requires the appropriate Raspberry Pi OS packages and a correctly connected Sense HAT.

Exact installed package versions are recorded in `docs/python-packages-week-03.txt` and `docs/python-packages-week-06.txt`.

## Run the Weather Station

Activate the virtual environment:

```bash
cd ~/weather-station
source .venv/bin/activate
```

Run the real Sense HAT station with the deployed model:

```bash
python station.py --no-mqtt --model models/temperature_model.json
```

The station continuously collects observations until stopped with `Ctrl+C`.

For a short test:

```bash
python station.py --no-mqtt --model models/temperature_model.json --samples 8
```

The first four valid readings warm up the feature window. A forecast becomes available once five continuous valid readings have been collected and the model accepts the input.

## Run the Dashboard

Open a second Raspberry Pi terminal:

```bash
cd ~/weather-station
source .venv/bin/activate
python webapp.py
```

The dashboard listens on `127.0.0.1:5000`.

For remote access, use VS Code Remote-SSH port forwarding or an SSH tunnel. Do not expose the Flask development server directly to a public network.

The dashboard shows measurements, observation freshness, context explanations, experimental forecasts and LED display controls.

## MQTT Classroom Demonstration

MQTT is optional and was used to demonstrate Pi-to-PC transmission.

To start the broker temporarily:

```bash
sudo systemctl start mosquitto
```

Run `station.py` without `--no-mqtt` to enable publishing.

The classroom broker configuration uses anonymous, unencrypted MQTT. It is not suitable for production deployment.

Stop the broker after testing:

```bash
sudo systemctl stop mosquitto
sudo systemctl disable mosquitto
```

## Testing

Run the automated tests:

```bash
python -m unittest discover -s tests -v
```

The latest recorded run completed 25 tests successfully.

These tests cover observation validation, storage, context calculations, model input checks and Flask web controls.

## Evaluation

The Ridge model was trained on 972 recorded Sense HAT observations.

On the held-out test set:

| Model | MAE |
|---|---:|
| Persistence baseline | 0.1012°C |
| Ridge Regression | 0.0900°C |

Three Raspberry Pi benchmark runs recorded median inference times between approximately 0.0145 and 0.0148 milliseconds.

These benchmarks measure model inference only, not end-to-end system latency or electrical power consumption.

## Project Files

- `station.py` – sensor sampling and main application loop
- `sensors.py` – real and simulated sensor access
- `common.py` – configuration and observation validation
- `storage.py` – SQLite storage
- `features.py` – five-reading feature calculations
- `context.py` – environmental state rules
- `mqtt_link.py` – MQTT publishing
- `model_runtime.py` – lightweight Ridge inference
- `matrix.py` – Sense HAT LED display
- `webapp.py` – Flask dashboard
- `timing.py` and `benchmark.py` – performance measurement
- `clear_retained.py` – retained MQTT message cleanup
- `models/` – exported temperature model
- `docs/` – weekly journals, reports and evidence

## Safety and Limitations

This is an educational indoor prototype, not a certified weather instrument, health monitor or warning system.

The Sense HAT temperature may be affected by Raspberry Pi self-heating. The model was trained on one device over a limited observation period.

MQTT traffic is not encrypted in the classroom configuration. Data exports, Windows copies and backups require separate retention decisions.

Predictions run in shadow mode and do not control environmental alerts.

Refer to `docs/model-card.md`, `docs/benchmark.md` and `docs/final-review.md` for detailed evaluation and limitations.
