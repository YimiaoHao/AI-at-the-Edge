# Week 5 – Deploy and Evaluate a Small Model

## Objective

This week, I aimed to train a small machine learning model on real Sense HAT data, deploy it to the Raspberry Pi and evaluate its accuracy and runtime performance.

## Work Completed

I copied the real sensor database from the Raspberry Pi to my Windows PC and used Python, NumPy and Scikit-learn to train a Ridge Regression model.

The dataset contained 972 observations, including 971 valid readings. After checking continuity and splitting the data chronologically, I obtained 661 training examples, 130 validation examples and 97 test examples.

I used six features from five consecutive readings to predict the temperature approximately 60 seconds ahead. I then exported the model as JSON and deployed it back to the Raspberry Pi.

I also updated `station.py` to run forecasts in shadow mode, created runtime measurements and tested model inference with real sensor data.

## Prediction and Results

I expected the model to produce forecasts after collecting five consecutive valid readings. I also expected it to reject invalid or incompatible input data.

On the test dataset, Ridge Regression achieved an MAE of 0.0900°C, compared with 0.1012°C for the persistence baseline. This represented an improvement of approximately 11.1%.

During an eight-reading live Sense HAT test, the first four readings produced no predictions because the feature window was incomplete. Readings 5–8 produced forecasts successfully.

All 21 unit tests passed, including tests for invalid measurements, missing features and incompatible data sources.

## Edge Performance

I ran three independent benchmarks with 1,000 inference iterations each.

Median inference latency ranged from 0.014500 to 0.014778 milliseconds, while P95 latency ranged from 0.015020 to 0.015372 milliseconds.

The model ran without requiring Scikit-learn on the Raspberry Pi. Runtime measurements were also recorded in `data/runtime.csv`.

## Problems and Limitations

One problem I encountered was that the Raspberry Pi initially could not import `model_runtime.py`, and the model JSON file was also missing. I checked the file paths and copied the missing files from Windows. The model then loaded successfully.

The model was trained using data from a single Sense HAT device and a limited recording period. The sensor temperature may be affected by heat from the Raspberry Pi.

The benchmark measured model inference only. It did not include sensor reading, database writes or network transmission, and it cannot establish electrical power consumption.

## Reflection

This week helped me understand the full process of training, exporting and deploying a small machine learning model to an edge device.

I learned why chronological data splitting and training-only preprocessing are important, why a simple persistence baseline is useful, and why model accuracy should be considered alongside input coverage and reliability.

I also learned that a model should refuse unsuitable inputs rather than producing misleading predictions. The existing sensor collection and context rules should continue working even when the model is unavailable.

My next step is to build a clear local dashboard in Week 6 so users can understand the station's measurements, environmental states and experimental predictions.