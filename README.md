# ⛈️ NWS Storm Prediction Center Outlook for Home Assistant
[![hacs_badge](https://img.shields.io/badge/HACS-Default-41BDF5.svg?style=for-the-badge)](https://github.com/hacs/integration)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/sedward5/nws_spc_outlook?style=for-the-badge)
![Maintenance](https://img.shields.io/maintenance/yes/2025?style=for-the-badge)
![GitHub License](https://img.shields.io/github/license/sedward5/nws_spc_outlook?style=for-the-badge)
![GitHub Downloads (all assets, all releases)](https://img.shields.io/github/downloads/sedward5/nws_spc_outlook/total?style=for-the-badge)
![Black Code Style](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge)
[![Buy me a coffee](https://img.shields.io/badge/buy_me_a_coffee-FFDD00?style=for-the-badge&logo=buy-me-a-coffee&logoColor=black)](https://buymeacoffee.com/sedward5)

A home assistant integration to poll weather outlook information from the NWS Storm Prediction Center

## 🔮 Sensors and Attributes
```
sensor.spc_outlook_day_1 # Returns categorical probability or "No Severe Weather"
│── Hail Probability
sensor.spc_outlook_day_2
sensor.spc_outlook_day_3
```

## 📁 File structure
```
custom_components/nws_spc_outlook/
│── __init__.py          # Handles setup and integration lifecycle
│── coordinator.py       # Handles data fetching and updates
│── sensor.py            # Defines sensor entities and data presentation
│── api.py               # Handles API requests and processing
│── const.py             # Stores constants like URLs
│── manifest.json        # Defines integration metadata
```

## ⚖️ Disclamer
This project and its author are in no way affialted with the National Weather Service. This addon should not be used as your sole source of information for severe weather preparedness. Stay informed, have a plan, be prepared.
