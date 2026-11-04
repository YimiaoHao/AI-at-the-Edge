# Week 7 – Data Retention Policy

## Purpose

This policy explains why the weather station stores data, how long different records are needed and how they should be removed.

## Retention Rules

| Data | Location | Retention and Removal |
|---|---|---|
| Real sensor observations | Pi `data/weather.db` | Seven-day project setting; expired records are removed during periodic cleanup while the station runs |
| Simulated observations | Pi `data/simulated.db` | Used only for software testing; expired records can be purged separately |
| Central observations | Windows PC `data/central.db` | Requires a separate retention check and cleanup |
| Training dataset copy | Windows PC `data/weather.db` | Retained only while needed for coursework and reproducibility |
| CSV exports | Pi or PC `data/` | Reviewed and removed separately when no longer required |
| Runtime logs | Pi `data/runtime.csv` | Bounded by log rotation, with one previous copy retained |
| MQTT retained messages | Mosquitto broker | Cleared explicitly after testing |
| Model and evaluation files | Project `models/` | Retained as coursework evidence while justified |

## Cleanup Procedure

Before deleting or purging data, I should stop the station and any receiver or web service that may still be using the relevant files.

I should first verify automated expiry using the simulated database rather than destroying useful real observations.

For SQLite data, the project provides a purge function that removes records older than the configured retention period.

MQTT retained messages, CSV exports, Windows databases, model files and backups require separate review because SQLite cleanup does not affect them.

## Verification

After cleanup, I should inspect the remaining database records, confirm the intended files or broker messages have been removed and record the result.

Deleting an SQLite record or file does not prove secure forensic erasure from storage media.

## Limitations

The seven-day setting is a classroom project choice, not a universal GDPR retention requirement.

Periodic cleanup depends on the program running. It does not guarantee that expired data disappears immediately at the seven-day boundary.

The policy must be reviewed if the collection purpose, users, deployment environment or legal requirements change.
