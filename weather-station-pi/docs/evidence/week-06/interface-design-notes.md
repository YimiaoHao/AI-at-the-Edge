# Week 6 – Interface Design and Improvement Notes

## Reconstructed Interface Sketch

This sketch was reconstructed after implementation to explain the interface structure. It is not an original pre-development sketch.

```text
+--------------------------------------------------+
| Local Weather Station                            |
| Station ID / Sensor Source                       |
| Educational-use notice                           |
+--------------------------------------------------+
| What is happening?                               |
| Context state and explanation                    |
| Pause dashboard updates / Refresh               |
+--------------------------------------------------+
| Measurements and context                         |
| Temperature | Humidity | Pressure                |
| Data age | Observation time | MQTT status        |
+--------------------------------------------------+
| Experimental prediction                          |
| Ridge forecast / Persistence baseline            |
+--------------------------------------------------+
| Control the physical display                     |
| Pause LED alerts / Resume display                |
| Last applied display state                       |
+--------------------------------------------------+
| Where the data goes                              |
| Storage, network and privacy limitations         |
+--------------------------------------------------+
```

## Interface Improvement

The initial functional interface was based on terminal output, where each observation appeared as a long JSON record. This was difficult to scan and required technical knowledge to interpret.

The final Flask dashboard groups information into labelled sections and readable cards. It displays measurement values, observation age, context explanations, experimental forecasts and physical display controls.

The improvement also introduced automatic text updates without rebuilding the page.

## Before and After

| Aspect | Before: Terminal Interface | After: Flask Dashboard |
|---|---|---|
| Measurements | Long JSON records | Labelled cards with units |
| Context state | Embedded in JSON | Clearly displayed with an explanation |
| Prediction | Numeric field in JSON | Separate forecast and baseline section |
| Freshness | Timestamp required manual interpretation | Observation age and stale-data handling |
| Controls | Mainly terminal commands | Browser buttons and hardware acknowledgement |
| Accessibility | Requires reading terminal output | Keyboard navigation, responsive layout and text labels |

## Evidence

- `week06-dashboard-final.png`: actual dashboard overview.
- `week06-dashboard-controls.png`: actual prediction, controls and data information.
- `docs/week-06.md`: implementation and testing record.

## Limitations

The reconstructed sketch is explanatory documentation rather than evidence of an original design sketch.

The before/after comparison describes a genuine change from terminal-based observation to the Flask dashboard, but no original terminal-interface screenshot has been archived here.

Further feedback from independent users would be needed to assess whether the interface is consistently understandable.
