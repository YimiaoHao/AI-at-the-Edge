# Privacy Notice – Local Weather Station

## What does this system do?

This Raspberry Pi weather station is an educational prototype. It measures indoor temperature, relative humidity and atmospheric pressure using a Sense HAT sensor.

The system also calculates an environmental state and provides experimental temperature predictions.

## What information is collected?

The station records:

- Temperature, humidity and pressure readings.
- Measurement timestamps and a device identifier (`station01`).
- Data validity information, environmental states and experimental predictions.

The system does not intentionally collect names, images, audio or information about who is present in a room.

However, timestamps and location information could potentially be used to infer human activity if combined with other information.

## Where is the data stored?

Observations are stored in a SQLite database on the Raspberry Pi.

During the classroom networking exercise, readings were also transmitted to a Windows PC and stored in a separate database.

Copies of the data may exist in exported CSV files, training datasets, model evaluation files and backups.

## How is the data transmitted?

The local dashboard is accessed through an SSH tunnel.

During MQTT experiments, the station used a classroom Mosquitto broker on port 1883 without transport encryption or authentication.

The MQTT broker is normally stopped when the experiment is not running.

No cloud service is required for the station's main functions.

## How long is the data kept?

The project uses a seven-day retention setting for local observations, with periodic cleanup while the station is running.

Other copies, such as Windows databases, CSV exports and training files, require separate review and deletion.

This setting does not guarantee immediate or secure erasure of all copies.

## What are the limitations?

The station is not a certified weather instrument, medical device or official warning system.

Temperature readings may be affected by heat from the Raspberry Pi. The machine learning model was trained on data from one sensor over a limited period.

Predictions and environmental states should not be used for health, safety or attendance decisions.

## Responsible Use

This prototype should only be used for learning, testing and demonstrating edge computing.

Before wider deployment, the system would require stronger security, clearer access controls, appropriate data retention procedures and further validation.
