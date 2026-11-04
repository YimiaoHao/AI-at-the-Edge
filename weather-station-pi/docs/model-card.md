# Model Card – Temperature Forecast

## Model Overview

This project uses Ridge Regression to predict Sense HAT temperature approximately 60 seconds ahead. The model runs locally on a Raspberry Pi 4 in shadow mode, meaning that its predictions do not control the environmental alerts.

## Training Data

The dataset contains 972 real Sense HAT observations collected at approximately five-second intervals. After checking data validity and continuity, the experiment used 661 training examples, 130 validation examples and 97 test examples.

Six input features were used: current temperature, humidity, pressure, five-reading mean temperature, five-reading mean humidity and temperature change.

## Evaluation Results

| Metric | Persistence Baseline | Ridge Regression |
|---|---:|---:|
| Test MAE | 0.1012°C | 0.0900°C |
| Test RMSE | 0.1275°C | 0.1122°C |

The Ridge model reduced test MAE by approximately 11.1% compared with the persistence baseline.

## Deployment

The model was exported as a JSON file and loaded on the Raspberry Pi without requiring Scikit-learn for inference. In a real Sense HAT test, the first four observations produced no prediction while the five-reading window was warming up. The next four observations produced forecasts successfully.

## Safety and Limitations

The model checks the data source, station ID, sampling interval and input validity before prediction. Unsupported inputs result in no prediction rather than a misleading value.

The dataset comes from one sensor and a limited collection period. Temperature measurements may be influenced by heat from the Raspberry Pi. The model has not been validated across different devices, seasons or locations.

Predictions are experimental and must not be treated as official weather forecasts, health advice or safety warnings.

## Intended Use

Educational demonstration of lightweight machine learning at the edge, including model deployment, baseline comparison, performance measurement and safe abstention.
