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
│── hail_probability:    # x or No Data
│── wind_probability:    # x or No Data
│── tornado_probability:  # x or No Data
│── friendly_name:        # SPC Outlook Day 1
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

## 🖱️ UI Example

This is a possible layout utilizing these sensors. This requires mushroom cards from HACS. 

```yaml
type: vertical-stack
cards:
  - type: grid
    columns: 4
    square: false
    cards:
      - type: markdown
        content: "**Risk**"
        layout: vertical
      - type: markdown
        content: "**Day 1**"
      - type: markdown
        content: "**Day 2**"
      - type: markdown
        content: "**Day 3**"
  - type: grid
    columns: 4
    square: false
    cards:
      - type: custom:mushroom-template-card
        icon: mdi:weather-lightning
        icon_color: white
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_1_outlook_day
        primary: "{{ states('sensor.spc_outlook_day_1') }}"
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_2
        primary: "{{ states('sensor.spc_outlook_day_2') }}"
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_3
        primary: "{{ states('sensor.spc_outlook_day_3') }}"
        layout: vertical
        fill_container: true
  - type: grid
    columns: 4
    square: false
    cards:
      - type: custom:mushroom-template-card
        icon: mdi:weather-windy
        icon_color: cyan
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_1
        primary: "{{ state_attr('sensor.spc_outlook_day_1', 'wind_probability') }}"
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_2
        primary: "{{ state_attr('sensor.spc_outlook_day_2', 'wind_probability') }}"
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        icon: mdi:border-none-variant
        layout: vertical
        fill_container: true
  - type: grid
    columns: 4
    square: false
    cards:
      - type: custom:mushroom-template-card
        icon: mdi:weather-tornado
        icon_color: red
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_1
        primary: "{{ state_attr('sensor.spc_outlook_day_1', 'tornado_probability') }}"
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_2
        primary: "{{ state_attr('sensor.spc_outlook_day_2', 'tornado_probability') }}"
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        entity: sensor.nws_outlook_day_3
        icon: mdi:border-none-variant
        layout: vertical
        fill_container: true
  - type: grid
    columns: 4
    square: false
    cards:
      - type: custom:mushroom-template-card
        icon: mdi:weather-hail
        icon_color: blue
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_1
        primary: "{{ state_attr('sensor.spc_outlook_day_1', 'hail_probability') }}"
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_2
        primary: "{{ state_attr('sensor.spc_outlook_day_2', 'hail_probability') }}"
        layout: vertical
        fill_container: true
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_3
        icon: mdi:border-none-variant
        layout: vertical
        fill_container: true
```

## 💻 Contributing

I'll be the first to admit I'm no developer. Feel free to submit issues and pull requests to improve this integration. See the [api guide](https://sedward5.github.io/nws_spc_outlook/nws_spc_outlook.html) to get started. 

## ⚖️ Disclamer
This project and its author are in no way affialted with the National Weather Service. This addon should not be used as your sole source of information for severe weather preparedness. Stay informed, have a plan, be prepared.
