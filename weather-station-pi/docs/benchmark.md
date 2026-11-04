# Week 5 – Edge Inference Benchmark

## Objective

The aim was to measure how efficiently the trained Ridge Regression model runs on the Raspberry Pi 4 and assess whether it is suitable for lightweight edge inference.

## Test Setup

- **Device:** Raspberry Pi 4
- **Model:** Ridge Regression, exported as JSON
- **Task:** Predict Sense HAT temperature approximately 60 seconds ahead
- **Runtime:** Pure Python inference
- **Iterations:** 1,000 per run
- **Independent runs:** 3
- **Input:** A fixed representative test observation, not newly collected sensor data

Each benchmark measured the inference function after 20 warm-up calls.

## Benchmark Results

| Run | Median (ms) | P95 (ms) | Peak Process RSS (KB) |
|---|---:|---:|---:|
| 1 | 0.014778 | 0.015372 | 13,272 |
| 2 | 0.014528 | 0.015020 | 13,280 |
| 3 | 0.014500 | 0.015074 | 13,264 |

The median inference time was consistently around 0.015 milliseconds. The results were similar across all three runs, suggesting stable performance for this fixed input and test environment.

## What Was Measured

The benchmark measured the execution time of `model.infer()` and recorded process CPU time and maximum resident memory.

The memory measurement represents the Python process, not the model alone.

The timed operation did not include Sense HAT sensor reads, feature calculation, SQLite writes, MQTT communication or the complete station sampling loop.

## Real Sensor Test

I also ran the model with eight real Sense HAT observations using `station.py`.

The first four readings produced no forecast because the five-reading feature window was incomplete. Readings 5–8 generated valid forecasts.

Four inference timing records were saved in `data/runtime.csv`, with durations between approximately 0.030 and 0.094 milliseconds.

## Limitations

The test used a fixed representative input and a relatively small number of benchmark runs. It therefore does not establish worst-case latency under heavy system load.

The results also do not measure end-to-end system latency or electrical power consumption. Separate hardware measurements would be needed to make claims about energy efficiency.

## Conclusion

The Ridge model demonstrated very low inference latency on the Raspberry Pi 4. This supports its suitability for the educational edge-computing prototype, but further testing would be needed before making broader performance or power-efficiency claims.
