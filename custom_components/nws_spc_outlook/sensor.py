import logging
from datetime import timedelta
import requests
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=30)
NWS_API_URL = "https://api.weather.gov/alerts/active/zone/{zone}"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_LATITUDE): cv.latitude,
    vol.Required(CONF_LONGITUDE): cv.longitude,
})

def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the NWS SPC Outlook sensor platform."""
    latitude = config[CONF_LATITUDE]
    longitude = config[CONF_LONGITUDE]

    coordinator = NWSSPCOutlookDataCoordinator(hass, latitude, longitude)
    add_entities([NWSSPCOutlookSensor(coordinator, day) for day in [1, 2, 3]])

class NWSSPCOutlookSensor(Entity):
    """Representation of an SPC Outlook sensor for each day."""

    def __init__(self, coordinator, day):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._day = day
        self._state = None
        self._attributes = {}

    @property
    def name(self):
        return f"SPC Outlook Day {self._day}"

    @property
    def state(self):
        return self._state

    @property
    def extra_state_attributes(self):
        return self._attributes

    def update(self):
        self._coordinator.update()
        data = self._coordinator.data.get(self._day)
        if data:
            self._state = data.get("overall_probability")
            self._attributes = {
                "hail_probability": data.get("hail_probability"),
                "wind_probability": data.get("wind_probability"),
                "tornado_probability": data.get("tornado_probability"),
            }

class NWSSPCOutlookDataCoordinator(DataUpdateCoordinator):
    """Fetches data from the NWS API."""

    def __init__(self, hass, latitude, longitude):
        super().__init__(hass, _LOGGER, name="NWS SPC Outlook", update_interval=SCAN_INTERVAL)
        self.latitude = latitude
        self.longitude = longitude

    def fetch_outlook_data(self):
        # TODO: Replace with real NWS API fetching code.
        return {
            1: {"overall_probability": "15%", "hail_probability": "10%", "wind_probability": "15%", "tornado_probability": "5%"},
            2: {"overall_probability": "5%", "hail_probability": "5%", "wind_probability": "5%", "tornado_probability": "2%"},
            3: {"overall_probability": "1%", "hail_probability": "1%", "wind_probability": "1%", "tornado_probability": "1%"}
        }

    async def _async_update_data(self):
        try:
            return self.fetch_outlook_data()
        except Exception as error:
            raise UpdateFailed(f"Error fetching data: {error}")
