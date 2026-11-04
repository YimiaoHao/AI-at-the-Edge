# Week 7 – Legal, Ethical and Societal Review

## Purpose

This review examines practical risks in my Raspberry Pi weather station. I connect each concern to evidence from the system, identify possible harms and explain what still needs improvement.

The risk ratings below are qualitative judgements for this classroom prototype, not formal compliance assessments.

## Risk Assessment

| Concern | Affected People and Possible Harm | Risk | Evidence and Existing Measures | Remaining Limitation |
|---|---|---|---|---|
| Privacy and purpose | A person using a monitored room could be indirectly identified through timestamps or a descriptive station name. | Medium | The project uses the neutral ID `station01` and records environmental measurements rather than names. | Time patterns and location information may still support inferences about occupancy. |
| Security | Another person on the same network could read MQTT messages or publish misleading data. | High | Mosquitto was configured for a classroom test and stopped after the experiment. Flask is restricted to localhost and accessed through SSH forwarding. | The classroom MQTT route uses anonymous, unencrypted communication. |
| Transparency and control | Users might mistake outdated readings or unacknowledged LED requests for current system behaviour. | Medium | The dashboard checks freshness, explains context states and records display acknowledgements. Stale-data and control tests passed. | Additional user testing is needed to confirm that explanations are understood. |
| Fairness and placement | People in different parts of a room might receive an unrepresentative temperature estimate. | Medium | The dashboard identifies the readings as an indoor prototype, and the model card describes device heating. | The Sense HAT is mounted on the Raspberry Pi, which may affect temperature measurements. |
| Reliability and over-trust | Someone might treat experimental temperature predictions or heat-index values as official warnings. | High | Ridge predictions run in shadow mode, unsuitable inputs are rejected, and the dashboard includes limitations. | The model was trained on one device and a limited observation period. |
| Accessibility and exclusion | Users with visual or motor difficulties might struggle to operate the interface. | Medium | I tested keyboard navigation, 200% zoom and narrow-screen layout. The interface uses text alongside colour and symbols. | Testing with users who have different accessibility needs has not been completed. |
| Sustainability | Continuous sampling, stored logs and long-running services consume storage and computing resources. | Low | The project uses five-second sampling, a seven-day retention setting and bounded runtime logs. | Electrical power use and the long-term resource impact have not been measured. |

## Risk Prioritisation

I rate the unencrypted MQTT connection and possible over-trust in predictions as high-priority concerns because they could lead to misleading data or inappropriate use.

Privacy, accessibility and transparency require further testing and clearer operating policies.

The system should remain a controlled educational prototype until these limitations are addressed.

## Trade-offs

Local processing reduces the need to send every measurement to a cloud service, but it does not eliminate privacy or security risks.

A simple Ridge model is fast to run, but low inference latency alone does not prove low energy consumption.

Strict rejection rules improve reliability but may reduce prediction coverage.

## Conditions Before Wider Deployment

Before wider use, I would require authenticated and encrypted communication, controlled file access, clear retention procedures, independent sensor validation and further accessibility testing.

I would also document how users can understand, challenge or stop the system's data processing.

## Reflection

This review helped me understand that responsible AI is not only about prediction accuracy. It also depends on data handling, system security, clear explanations, appropriate user control and the limits of available evidence.
