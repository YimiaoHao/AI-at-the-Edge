# Week 6 – Build a Calm, Understandable Interface

## Objective

This week, I aimed to make the weather station easier to understand by adding a physical LED display and a local web dashboard.

## Work Completed

I created `matrix.py` to show environmental states on the Sense HAT LED matrix and updated `station.py` to control the display. I also developed a Flask dashboard using `webapp.py`, `templates/index.html`, `static/style.css` and `static/dashboard.js`.

The dashboard shows sensor readings, context explanations and experimental temperature predictions. It also provides automatic updates and controls for pausing dashboard updates or temporarily muting visual alerts.

I implemented and tested these features myself.

## Prediction and Results

I expected that pausing the visual alerts would not stop sensor measurements or change the trained model.

During testing, the LED changed from the warming-up symbol to the attention symbol. The webpage opened successfully through SSH port forwarding and updated automatically.

I tested the two pause functions separately. Pausing dashboard updates froze the browser values while the station continued collecting data. Pausing visual alerts changed the LED display to muted, and the database recorded the applied state.

All 25 unit tests passed.

## Failure and Accessibility Testing

I stopped `station.py` while keeping Flask running. After the freshness limit, the dashboard marked the readings as stale, showed unavailable measurements and explained why they were no longer current.

I also tested keyboard navigation, 200% browser zoom and narrow-screen layout. The controls remained usable, and the content was readable.

These checks helped me understand why a dashboard must communicate failures clearly rather than simply keep showing old values.

## Design Choices and Limitations

I used text and symbols alongside colours so that users do not have to rely only on colour to understand the environmental state.

Only `station.py` directly controls the Sense HAT hardware. Flask sends requests through SQLite, and the station records acknowledgement after applying the requested display state.

The webpage runs locally through an SSH tunnel. It is a teaching prototype rather than a production-ready public web service.

## Reflection

This week taught me that a useful interface should be understandable, accessible and honest about data quality.

I also learned the difference between pausing displayed information and pausing physical alerts. Neither action should interrupt the main sensor collection process.

The next step is to review data privacy, security, retention and responsible use in Week 7.
