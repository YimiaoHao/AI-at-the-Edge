# AI at the Edge – Evidence Index

## Purpose

This folder contains supporting evidence for the Raspberry Pi Sense HAT weather station project. It links experimental results, screenshots and explanatory notes to the work completed during Weeks 5–7.

The main source code and weekly learning journals remain in the project root and `docs` directory.

## Week 5 – Model Training and Edge Performance

Location: `week-05/`

| File | Evidence |
|---|---|
| `temperature_model.report.json` | Ridge model evaluation, baseline comparison and chronological split |
| `temperature_model.cases.json` | Individual predictions for the held-out test examples |
| `python-packages-week-05.txt` | Recorded Windows training environment |
| `benchmark-run-1.json` | First Raspberry Pi inference benchmark |
| `benchmark-run-2.json` | Second Raspberry Pi inference benchmark |
| `benchmark-run-3.json` | Third Raspberry Pi inference benchmark |
| `runtime.csv` | Logged inference timings during station operation |

The Ridge model achieved a test MAE of approximately 0.0900°C, compared with 0.1012°C for the persistence baseline.

## Week 6 – Interface and Usability

Location: `week-06/`

| File | Evidence |
|---|---|
| `week06-dashboard-final.png` | Real Flask dashboard showing sensor readings, context and data freshness |
| `week06-dashboard-controls.png` | Real dashboard showing prediction, display controls and acknowledgement |
| `interface-design-notes.md` | Reconstructed interface sketch and terminal-to-dashboard comparison |

The interface was tested for stale data, keyboard use, narrow-screen layout, browser zoom and two different pause functions.

The reconstructed sketch is explanatory documentation, not an original pre-development design record.

## Week 7 – Responsible Use and Data Cleanup

Location: `week-07/`

| File | Evidence |
|---|---|
| `cleanup-test-evidence.md` | Recorded simulated-database retention test and MQTT retained-message cleanup |

The MQTT broker acknowledged the clearing of the station's retained telemetry and status messages. New subscriptions did not receive those retained messages, and Mosquitto was subsequently stopped.

The simulated database test removed zero expired rows and retained 28 recent observations. It does not independently demonstrate deletion of expired records.

## Other Supporting Files

- `docs/week-02.md` to `docs/week-07.md`: weekly learning journals.
- `docs/model-card.md`: model purpose, evaluation and limitations.
- `docs/benchmark.md`: Raspberry Pi performance summary.
- `docs/data-flow.md`: complete data lifecycle.
- `docs/lesi-review.md`: legal, ethical and societal risk review.
- `docs/retention.md`: data retention policy.
- `docs/privacy-notice.md`: user-facing privacy explanation.
- `docs/final-review.md`: final responsible-use reflection.
- `tests/`: automated tests for core functions, context, model and Flask dashboard.

## Evidence Limitations

Some results are preserved as structured files rather than screenshots. The Week 6 design sketch was reconstructed after implementation.

The evidence supports specific tested behaviour, not production readiness, complete accessibility conformance, secure deletion of every data copy or measured electrical power efficiency.
