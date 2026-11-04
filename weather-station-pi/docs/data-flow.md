# Week 7 – Data Lifecycle and Data Flow

## Purpose

This document describes how data moves through my Raspberry Pi weather station and identifies possible privacy and security risks.

## Data Collection

The Sense HAT measures temperature, relative humidity and atmospheric pressure approximately every five seconds.

Each observation includes a station ID, timestamp, sensor source, measurement values and validity information. The station uses the neutral identifier `station01`.

## Data Flow

| From | To | Data and Purpose | Security and Access |
|---|---|---|---|
| Sense HAT | Raspberry Pi station.py | Sensor measurements for local processing | Local hardware connection; physical access matters |
| station.py | Pi SQLite database | Observations, context and forecasts for storage and review | Local file, not encrypted by the application |
| station.py | Sense HAT LED | Context state for physical display | Direct hardware control by the station process |
| Pi SQLite database | Flask dashboard | Latest readings, explanations and forecasts | Flask listens on localhost; remote browser uses SSH forwarding |
| Raspberry Pi | Mosquitto broker | MQTT telemetry and status messages when enabled | Classroom configuration uses anonymous, unencrypted MQTT on port 1883 |
| Mosquitto broker | Windows PC receiver | Telemetry for validation and central SQLite storage | Access depends on the trusted local network |
| Pi data | Windows training project | Copied historical observations for model training | File transfer over SSH/SCP |
| Windows training project | Raspberry Pi | Exported Ridge model JSON for local inference | Transferred over SSH/SCP |

## Stored Files

The Raspberry Pi stores observations in `data/weather.db` and simulation data separately in `data/simulated.db`.

The Windows receiver stores received observations in `data/central.db`. A separate Windows training project also contains a copied `weather.db`.

Model files and training reports are stored in the project's `models` directory. Runtime logs, benchmark results and any exported CSV files are additional copies that require separate retention decisions.

## Privacy and Security Risks

Environmental measurements are not automatically personal data, but station identifiers, locations and timestamps may reveal information about people when combined with other knowledge.

The classroom MQTT configuration does not use authentication or transport encryption. The SSH tunnel protects remote browser access, but it does not encrypt separate MQTT traffic.

Local processing reduces the need for cloud transmission, but local files, backups and physical access still require protection.

## Boundaries

This prototype is intended for educational indoor environmental monitoring. It is not designed to identify individuals, infer room attendance or provide official weather or health warnings.

Changing a device name alone does not guarantee anonymity. Data minimisation, restricted access, clear retention rules and secure communication would be necessary before wider deployment.
