# UI Example

You can utilize these sensors to build a number of dashboards and automations. This example requires [mushroom](https://github.com/piitaya/lovelace-mushroom) and [card_mod](https://github.com/thomasloven/lovelace-card-mod). It takes advantage of the color hex codes used by SPC and puts the timestamps in local time. 

![Example of a grid view](ui-example.jpeg)

```yaml
type: vertical-stack
cards:
  - type: grid
    columns: 4
    square: false
    cards:
      - type: markdown
        content: "**Risk**"
      - type: custom:mushroom-template-card
        primary: Day 1
        fill_container: true
        secondary: >-
          {{ as_local(strptime(state_attr('sensor.spc_outlook_day_1',
          'valid')+'+0000', '%Y%m%d%H%M%z')).strftime('%a %d %H:%M') }}

          {{ as_local(strptime(state_attr('sensor.spc_outlook_day_1',
          'expire')+'+0000', '%Y%m%d%H%M%z')).strftime('%a %d %H:%M') }}
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-secondary-font-size: 9px;
              }
              .secondary { 
                white-space: break-spaces !important;
                word-wrap: break-word;
                overflow-wrap: break-word;

                -webkit-hyphens: auto;
                -moz-hyphens: auto;
                hyphens: auto;
              }
      - type: custom:mushroom-template-card
        primary: Day 2
        fill_container: true
        secondary: >-
          {{ as_local(strptime(state_attr('sensor.spc_outlook_day_2',
          'valid')+'+0000', '%Y%m%d%H%M%z')).strftime('%a %d %H:%M') }}

          {{ as_local(strptime(state_attr('sensor.spc_outlook_day_2',
          'expire')+'+0000', '%Y%m%d%H%M%z')).strftime('%a %d %H:%M') }}
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-secondary-font-size: 9px;
              }
              .secondary { 
                white-space: break-spaces !important;
                word-wrap: break-word;
                overflow-wrap: break-word;

                -webkit-hyphens: auto;
                -moz-hyphens: auto;
                hyphens: auto;
              }
      - type: custom:mushroom-template-card
        primary: Day 3
        fill_container: true
        secondary: >-
          {{ as_local(strptime(state_attr('sensor.spc_outlook_day_3',
          'valid')+'+0000', '%Y%m%d%H%M%z')).strftime('%a %d %H:%M') }}

          {{ as_local(strptime(state_attr('sensor.spc_outlook_day_3',
          'expire')+'+0000', '%Y%m%d%H%M%z')).strftime('%a %d %H:%M') }}
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-secondary-font-size: 9px;
              }
              .secondary { 
                white-space: break-spaces !important;
                word-wrap: break-word;
                overflow-wrap: break-word;

                -webkit-hyphens: auto;
                -moz-hyphens: auto;
                hyphens: auto;
              }
  - type: grid
    columns: 4
    square: false
    cards:
      - type: custom:mushroom-template-card
        icon: mdi:weather-lightning
        icon_color: white
        layout: vertical
        fill_container: true
        primary: Categorical
        tap_action:
          action: more-info
        card_mod:
          style:
            mushroom-shape-icon$: |
              .shape {
                --icon-symbol-size: 40px;
                --icon-size: 100px;
                left: -20px;
                top: -35px;
                margin-bottom: -80px;
                border-radius: 50% !important;
              }
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 10px;
                --card-primary-color: white;
              }
            .: |
              ha-card {
                overflow: hidden;
              }
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_1_outlook_day
        primary: "{{ states('sensor.spc_outlook_day_1') }}"
        layout: vertical
        fill_container: true
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 12px;
                {% if not is_state('sensor.spc_outlook_day_1', 'No Risk') %}
                --card-primary-color: black;
                {% endif %}
              }
              .primary { 
                white-space: normal !important;
                word-wrap: break-word;
                overflow-wrap: break-word;

                -webkit-hyphens: auto;
                -moz-hyphens: auto;
                hyphens: auto;
              }
            .: |
              ha-card {
                background-color: {{ state_attr('sensor.spc_outlook_day_1', 'categorical_fill') }}
              }
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_2
        primary: "{{ states('sensor.spc_outlook_day_2') }}"
        layout: vertical
        fill_container: true
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 12px;
                {% if not is_state('sensor.spc_outlook_day_2', 'No Risk') %}
                --card-primary-color: black;
                {% endif %}
              }
              .primary { 
                white-space: normal !important;
                word-wrap: break-word;
                overflow-wrap: break-word;

                -webkit-hyphens: auto;
                -moz-hyphens: auto;
                hyphens: auto;
              }
            .: |
              ha-card {
                background-color: {{ state_attr('sensor.spc_outlook_day_2', 'categorical_fill') }}
              }
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_3
        primary: "{{ states('sensor.spc_outlook_day_3') }}"
        layout: vertical
        fill_container: true
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 12px;
                {% if not is_state('sensor.spc_outlook_day_3', 'No Risk') %}
                --card-primary-color: black;
                {% endif %}
              }
              .primary { 
                white-space: normal !important;
                word-wrap: break-word;
                overflow-wrap: break-word;

                -webkit-hyphens: auto;
                -moz-hyphens: auto;
                hyphens: auto;
              }
            .: |
              ha-card {
                background-color: {{ state_attr('sensor.spc_outlook_day_3', 'categorical_fill') }}
              }
  - type: grid
    columns: 4
    square: false
    cards:
      - type: custom:mushroom-template-card
        icon: mdi:weather-windy
        icon_color: cyan
        layout: vertical
        fill_container: true
        primary: Wind
        card_mod:
          style:
            mushroom-shape-icon$: |
              .shape {
                --icon-symbol-size: 40px;
                --icon-size: 100px;
                left: -20px;
                top: -45px;
                margin-bottom: -80px;
                border-radius: 50% !important;
              }
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 10px;
                --card-primary-color: cyan;
              }
            .: |
              ha-card {
                overflow: hidden;
              }
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_1
        primary: "{{ state_attr('sensor.spc_outlook_day_1', 'wind_probability') }}"
        layout: vertical
        fill_container: true
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 12px;
                {% if state_attr('sensor.spc_outlook_day_1', 'wind_probability') != 'No Risk' %}
                --card-primary-color: black;
                {% endif %}
              }
              .primary { 
                white-space: normal !important;
              }
            .: |
              ha-card {
                background-color: {{ state_attr('sensor.spc_outlook_day_1', 'wind_fill') }}
              }
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_2
        primary: "{{ state_attr('sensor.spc_outlook_day_2', 'wind_probability') }}"
        layout: vertical
        fill_container: true
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 12px;
                {% if state_attr('sensor.spc_outlook_day_2', 'wind_probability') != 'No Risk' %}
                --card-primary-color: black;
                {% endif %}
              }
              .primary { 
                white-space: normal !important;
              }
            .: |
              ha-card {
                background-color: {{ state_attr('sensor.spc_outlook_day_2', 'wind_fill') }}
              }
      - type: vertical-stack
        cards:
          - type: custom:mushroom-template-card
            primary: Day 4
            secondary: "{{ states('sensor.spc_outlook_day_4') }}"
            card_mod:
              style:
                mushroom-state-info$: |
                  .container {
                    --card-primary-font-size: 12px;
                    --card-secondary-font-size: 9px;
                    {% if not is_state('sensor.spc_outlook_day_4', 'No Risk') %}
                    --card-primary-color: black;
                    --card-secondary-color: black;
                    {% endif %}
                  }
                  .primary { 
                    white-space: normal !important;
                    word-wrap: break-word;
                    overflow-wrap: break-word;

                    -webkit-hyphens: auto;
                    -moz-hyphens: auto;
                    hyphens: auto;
                  }
                .: |
                  ha-card {
                    background-color: {{ state_attr('sensor.spc_outlook_day_4', 'probabilistic_fill') }}
                  }
          - type: custom:mushroom-template-card
            primary: Day 5
            secondary: "{{ states('sensor.spc_outlook_day_5') }}"
            card_mod:
              style:
                mushroom-state-info$: |
                  .container {
                    --card-primary-font-size: 12px;
                    --card-secondary-font-size: 9px;
                    {% if not is_state('sensor.spc_outlook_day_5', 'No Risk') %}
                    --card-primary-color: black;
                    --card-secondary-color: black;
                    {% endif %}
                  }
                  .primary { 
                    white-space: normal !important;
                    word-wrap: break-word;
                    overflow-wrap: break-word;

                    -webkit-hyphens: auto;
                    -moz-hyphens: auto;
                    hyphens: auto;
                  }
                .: |
                  ha-card {
                    background-color: {{ state_attr('sensor.spc_outlook_day_5', 'probabilistic_fill') }}
                  }
  - type: grid
    columns: 4
    square: false
    cards:
      - type: custom:mushroom-template-card
        icon: mdi:weather-tornado
        icon_color: red
        layout: vertical
        fill_container: true
        primary: Tornado
        card_mod:
          style:
            mushroom-shape-icon$: |
              .shape {
                --icon-symbol-size: 40px;
                --icon-size: 100px;
                left: -20px;
                top: -45px;
                margin-bottom: -80px;
                border-radius: 50% !important;
              }
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 10px;
                --card-primary-color: red;
              }
            .: |
              ha-card {
                overflow: hidden;
              }
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_1
        primary: "{{ state_attr('sensor.spc_outlook_day_1', 'torn_probability') }}"
        layout: vertical
        fill_container: true
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 12px;
                {% if state_attr('sensor.spc_outlook_day_1', 'torn_probability') != 'No Risk' %}
                --card-primary-color: black;
                {% endif %}
              }
              .primary { 
                white-space: normal !important;
              }
            .: |
              ha-card {
                background-color: {{ state_attr('sensor.spc_outlook_day_1', 'torn_fill') }}
              }
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_2
        primary: "{{ state_attr('sensor.spc_outlook_day_2', 'torn_probability') }}"
        layout: vertical
        fill_container: true
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 12px;
                {% if state_attr('sensor.spc_outlook_day_2', 'torn_probability') != 'No Risk' %}
                --card-primary-color: black;
                {% endif %}
              }
              .primary { 
                white-space: normal !important;
              }
            .: |
              ha-card {
                background-color: {{ state_attr('sensor.spc_outlook_day_2', 'torn_fill') }}
              }
      - type: vertical-stack
        cards:
          - type: custom:mushroom-template-card
            primary: Day 6
            secondary: "{{ states('sensor.spc_outlook_day_6') }}"
            card_mod:
              style:
                mushroom-state-info$: |
                  .container {
                    --card-primary-font-size: 12px;
                    --card-secondary-font-size: 9px;
                    {% if not is_state('sensor.spc_outlook_day_6', 'No Risk') %}
                    --card-primary-color: black;
                    --card-secondary-color: black;
                    {% endif %}
                  }
                  .primary { 
                    white-space: normal !important;
                    word-wrap: break-word;
                    overflow-wrap: break-word;

                    -webkit-hyphens: auto;
                    -moz-hyphens: auto;
                    hyphens: auto;
                  }
                .: |
                  ha-card {
                    background-color: {{ state_attr('sensor.spc_outlook_day_6', 'probabilistic_fill') }}
                  }
          - type: custom:mushroom-template-card
            primary: Day 7
            secondary: "{{ states('sensor.spc_outlook_day_7') }}"
            card_mod:
              style:
                mushroom-state-info$: |
                  .container {
                    --card-primary-font-size: 12px;
                    --card-secondary-font-size: 9px;
                    {% if not is_state('sensor.spc_outlook_day_7', 'No Risk') %}
                    --card-primary-color: black;
                    --card-secondary-color: black;
                    {% endif %}
                  }
                  .primary { 
                    white-space: normal !important;
                    word-wrap: break-word;
                    overflow-wrap: break-word;

                    -webkit-hyphens: auto;
                    -moz-hyphens: auto;
                    hyphens: auto;
                  }
                .: |
                  ha-card {
                    background-color: {{ state_attr('sensor.spc_outlook_day_7', 'probabilistic_fill') }}
                  }
  - type: grid
    columns: 4
    square: false
    cards:
      - type: custom:mushroom-template-card
        icon: mdi:weather-hail
        icon_color: blue
        layout: vertical
        fill_container: true
        primary: Hail
        card_mod:
          style:
            mushroom-shape-icon$: |
              .shape {
                --icon-symbol-size: 40px;
                --icon-size: 100px;
                left: -20px;
                top: -40px;
                margin-bottom: -80px;
                border-radius: 50% !important;
              }
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 10px;
                --card-primary-color: #2196F2;
              }
            .: |
              ha-card {
                overflow: hidden;
              }
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_1
        primary: "{{ state_attr('sensor.spc_outlook_day_1', 'hail_probability') }}"
        layout: vertical
        fill_container: true
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 12px;
                {% if state_attr('sensor.spc_outlook_day_1', 'hail_probability') != 'No Risk' %}
                --card-primary-color: black;
                {% endif %}
              }
              .primary { 
                white-space: normal !important;
              }
            .: |
              ha-card {
               background-color: {{ state_attr('sensor.spc_outlook_day_1', 'hail_fill') }}
              }
      - type: custom:mushroom-template-card
        entity: sensor.spc_outlook_day_2
        primary: "{{ state_attr('sensor.spc_outlook_day_2', 'hail_probability') }}"
        layout: vertical
        fill_container: true
        card_mod:
          style:
            mushroom-state-info$: |
              .container {
                --card-primary-font-size: 12px;
                {% if state_attr('sensor.spc_outlook_day_2', 'hail_probability') != 'No Risk' %}
                --card-primary-color: black;
                {% endif %}
              }
              .primary { 
                white-space: normal !important;
              }
            .: |
              ha-card {
                background-color: {{ state_attr('sensor.spc_outlook_day_2', 'hail_fill') }}
              }
      - type: vertical-stack
        cards:
          - type: custom:mushroom-template-card
            primary: Day 8
            secondary: "{{ states('sensor.spc_outlook_day_8') }}"
            card_mod:
              style:
                mushroom-state-info$: |
                  .container {
                    --card-primary-font-size: 12px;
                    --card-secondary-font-size: 9px;
                    {% if not is_state('sensor.spc_outlook_day_8', 'No Risk') %}
                    --card-primary-color: black;
                    --card-secondary-color: black;
                    {% endif %}
                  }
                  .primary { 
                    white-space: normal !important;
                    word-wrap: break-word;
                    overflow-wrap: break-word;

                    -webkit-hyphens: auto;
                    -moz-hyphens: auto;
                    hyphens: auto;
                  }
                .: |
                  ha-card {
                    background-color: {{ state_attr('sensor.spc_outlook_day_8', 'probabilistic_fill') }}
                  }
          - type: custom:mushroom-template-card
            primary: ...
            card_mod:
              style:
                mushroom-state-info$: |
                  .container {
                    --card-primary-font-size: 12px;
                  }
                  .primary { 
                    white-space: normal !important;
                    word-wrap: break-word;
                    overflow-wrap: break-word;

                    -webkit-hyphens: auto;
                    -moz-hyphens: auto;
                    hyphens: auto;
                  }
                .: |
                  ha-card {
                    background-color: #000000;
                  }

```
