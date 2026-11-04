# AI at the Edge – Windows PC Project

## Project Overview

This is the Windows PC component of my Raspberry Pi Sense HAT weather station project for the AI at the Edge module.

It has two main purposes:

1. Receive and store weather station observations transmitted through MQTT.
2. Train, evaluate and export a lightweight machine learning model for deployment on the Raspberry Pi.

The Raspberry Pi handles sensor collection and live inference, while the Windows PC provides central data reception and model training.

## System Architecture

```text
Raspberry Pi + Sense HAT
        |
        v
station.py (MQTT publisher)
        |
        v
Mosquitto broker on Raspberry Pi
        |
        v
central_receiver.py (Windows PC)
        |
        v
data/central.db (SQLite)


data/weather.db (copied from Raspberry Pi)
        |
        v
train_model.py
        |
        v
Ridge Regression training and evaluation
        |
        v
models/temperature_model.json
        |
        v
Raspberry Pi edge inference
```

## Software Requirements

- Windows with Python 3.12
- NumPy and Scikit-learn for model training
- Paho MQTT for the receiver
- SQLite for local data storage

The training dependencies are listed in `requirements-training.txt`.

The exact installed Python packages used during the experiment are recorded in `docs/python-packages-week-05.txt`.

## Environment Setup

Open a terminal in the Windows project directory:

```cmd
cd /d D:\AAI_Project\weather-station-pc
```

Create and activate a virtual environment:

```cmd
py -3.12 -m venv .venv
.venv\Scripts\activate.bat
```

Install the training dependencies:

```cmd
python -m pip install -r requirements-training.txt
```

Install Paho MQTT if it is not already available:

```cmd
python -m pip install "paho-mqtt>=2.1,<3"
```

The Python launcher command may differ between computers. The project was tested using Python 3.12 on Windows.

## MQTT Receiver

The receiver connects to the Mosquitto broker running on the Raspberry Pi.

Check `config_pc.json` before connecting. Its `broker_host` must contain the Raspberry Pi's current IP address on the trusted local network.

Run:

```cmd
python central_receiver.py --config config_pc.json
```

The receiver subscribes to the station's MQTT topics, validates incoming observations and saves accepted records to `data/central.db`.

The Raspberry Pi must have its Mosquitto broker running and `station.py` publishing without the `--no-mqtt` option.

This classroom MQTT configuration uses anonymous, unencrypted communication and must not be exposed to an untrusted network.

## Training Data

The training dataset was copied from the Raspberry Pi's SQLite database to:

`data/weather.db`

The recorded dataset contained 972 observations from the real Sense HAT.

The training task was to predict sensor temperature approximately 60 seconds ahead using six features derived from five consecutive readings.

Training and evaluation used chronological data partitions to avoid random mixing of earlier and later observations.

## Inspect the Training Data

Run:

```cmd
python check_training_data.py
```

The previous data inspection reported:

- 972 database rows
- 971 valid readings
- Seven continuous segments
- 920 usable 60-second prediction examples before chronological partitioning

## Train the Model

Run:

```cmd
python train_model.py
```

The training script compares Ridge Regression with a persistence baseline, selects the Ridge regularisation parameter using validation data and evaluates performance on the held-out test set.

The recorded results were:

| Model | Test MAE | Test RMSE |
|---|---:|---:|
| Persistence baseline | 0.1012°C | 0.1275°C |
| Ridge Regression | 0.0900°C | 0.1122°C |

The selected Ridge alpha was `0.01`.

## Exported Files

The model training stage generated:

- `models/temperature_model.json` – exported inference model
- `models/temperature_model.report.json` – evaluation report
- `models/temperature_model.cases.json` – test predictions and evaluation cases

The runtime implementation in `model_runtime.py` allows the exported model to run on the Raspberry Pi without installing Scikit-learn there.

## Data and Model Limitations

The data came from one Sense HAT device over a limited period. Sensor temperature may be influenced by Raspberry Pi heating.

The results describe this particular chronological test split and do not establish accuracy across different devices, locations or environmental conditions.

The predictions are experimental and must not be used as official forecasts or safety warnings.

## Project Files

- `central_receiver.py` – MQTT subscriber and central data storage
- `check_training_data.py` – inspect data continuity and suitability
- `train_model.py` – chronological training, tuning and evaluation
- `model_runtime.py` – lightweight Ridge inference implementation
- `features.py` – shared feature definitions
- `common.py` – observation validation and configuration
- `storage.py` – SQLite storage
- `config_pc.json` – PC receiver configuration
- `config.json` – configuration for the copied weather database
- `requirements-training.txt` – training dependencies
- `data/` – received and copied observations
- `models/` – model and evaluation outputs
- `docs/` – environment records and supplementary evidence

## Responsible Use

The Windows database, copied training data and model evaluation files are separate copies from the Raspberry Pi database.

Deleting data from the MQTT broker or the Raspberry Pi does not automatically remove these Windows copies.

Data should be retained only where necessary for coursework and reproducibility, with appropriate access control and deletion procedures.
