# Week 3 – Send Observations to a PC

## Objective

The aim was to send Sense HAT observations from the Raspberry Pi to a Windows PC using MQTT, while maintaining local data storage.

## Work Completed

I configured Mosquitto and installed Paho MQTT 2.1.0. I created `mqtt_link.py`, updated `station.py`, and developed `central_receiver.py` on my Windows PC.

The data followed this route: Sense HAT → station.py → Mosquitto broker → PC receiver → SQLite database.

## Testing and Results

I expected the Pi to continue collecting data even when the PC or network was unavailable. During testing, the PC successfully saved six new observations and one retained message.

I also tested receiver interruption, broker shutdown and Wi-Fi disconnection. The Pi continued storing readings locally. After these tests, its database contained 972 observations.

## Problems and Limitations

I found that a successful MQTT connection does not guarantee that the PC has saved a message. Retained messages also do not automatically recover a complete missing history.

The experiment used anonymous, unencrypted MQTT on port 1883. This is suitable only for a controlled classroom demonstration, not a secure production deployment.

## What I Learned

I learned how publishers, brokers, subscribers and MQTT topics work together. I also learned the importance of local storage, message validation and testing network failures separately.