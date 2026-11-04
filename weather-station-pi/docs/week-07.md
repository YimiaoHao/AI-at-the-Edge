# Week 7 – Responsible Use of the Edge Weather Station

## Objective

This week, I reviewed the privacy, security, reliability and ethical limitations of my Raspberry Pi weather station. My aim was to connect these concerns to the system I actually built and tested.

## Work Completed

I documented the complete data lifecycle in `docs/data-flow.md`, including sensor collection, local SQLite storage, MQTT transmission, the Windows PC archive, model files and browser access.

I created `docs/lesi-review.md` to assess privacy, security, transparency, reliability, accessibility and sustainability risks.

I also wrote a data retention policy, a privacy notice and a final review. I completed the documentation and checks myself.

## Prediction and Actual Results

I expected that clearing MQTT retained messages would not delete the readings already stored in SQLite databases.

Before cleanup, I stopped the station and temporarily started Mosquitto. I ran `clear_retained.py` and received confirmation that the broker had acknowledged empty retained values.

I then used new MQTT subscriptions to check the telemetry and status topics. Neither returned a retained message. Finally, I stopped and disabled Mosquitto, confirming that the service was inactive.

## Retention Testing

I tested the retention command against the simulated database using `config_sim.json`.

The command removed zero expired rows, and all 28 recent simulated observations remained available. This confirmed that the command completed without removing recent records, but it did not independently demonstrate the removal of expired records.

## Risks and Limitations

One important security concern was the anonymous, unencrypted MQTT connection used during the classroom exercise. I addressed the immediate exposure by stopping the broker after testing, but this configuration would still require authentication and encryption before wider deployment.

I also recognised that clearing broker messages does not erase copies stored on the Raspberry Pi, Windows PC or exported files.

Other limitations include sensor heating, limited model validation, unmeasured electrical power consumption and incomplete accessibility evaluation.

## Reflection

This week helped me understand that responsible edge AI involves more than building a working system.

I learned the importance of mapping every data copy, explaining limitations honestly, testing deletion claims and considering how environmental measurements might reveal information about people.

Before a wider deployment, I would improve network security, verify data deletion across all storage locations and validate the sensor and model under different operating conditions.
