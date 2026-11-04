# Week 4 – Make the Readings Meaningful

## Objective

This week, I wanted to make the weather station more useful by analysing recent sensor readings instead of looking at each measurement separately.

## Work Completed

I created `features.py` to calculate six features from five consecutive valid readings. These include the current measurements, average temperature, average humidity and temperature change.

I also created `context.py` to classify the station's state as normal, attention, warming_up or unknown. I then updated `station.py` to use both modules while keeping the existing local database and MQTT functionality.

I implemented the changes and ran the tests myself.

## Prediction and Results

I expected the first four valid readings to return warming_up, because the feature window requires five samples.

In my first simulation, I collected eight readings. The first four returned warming_up, while readings 5–8 returned normal.

I also ran the unit tests. All 14 tests passed.

## Example Observation and Feature Window

One simulated observation from my first run was:

- Temperature: 25.80°C
- Humidity: 60.47%
- Pressure: 1012.19 hPa
- Valid: True

The five temperature readings in its feature window were approximately:

25.17, 25.36, 25.73, 25.83 and 25.80°C.

These produced:

- Mean temperature: 25.62°C
- Mean humidity: 59.41%
- Temperature change: +0.63°C

The resulting state was normal. The explanation reported five-reading averages of approximately 25.6°C and 59.4% relative humidity.

With a five-second sampling interval, five observations cover approximately 20 seconds between the first and last readings.

## Fault Testing

I tested invalid data using a 12-sample simulation with a fault introduced every seventh reading.

As expected, reading 7 was marked invalid and returned unknown. Readings 8–11 returned warming_up, and reading 12 returned normal after five new valid observations.

This confirmed that the feature window resets after an invalid reading instead of combining unreliable data with new measurements.

## Hysteresis and Limitations

The context policy uses hysteresis to prevent frequent changes between normal and attention when measurements fluctuate around a threshold.

In my implementation, attention is triggered when the five-reading mean temperature reaches 28°C or humidity exceeds 75%. It clears only when temperature falls below 26°C and humidity falls below 70%.

The heat-index calculation is restricted to temperatures from 27–40°C and relative humidity from 40–85%. Outside this range, the function returns no estimate rather than presenting an unsupported value.

These thresholds are classroom demonstration rules, not official weather warnings. The Sense HAT temperature may also be affected by heat from the Raspberry Pi.

## Reflection

This week helped me understand how recent measurements can provide more useful context than individual values. I learned that a feature window needs continuity checks, invalid data must be handled explicitly, and hysteresis can make environmental states more stable.

The main problem I investigated was how the system should recover after an invalid sensor reading. The simulation showed that the station could return to a meaningful state after collecting five new valid samples.

My next step is to use these features to train and evaluate a small temperature prediction model in Week 5.
