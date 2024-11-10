import logging
from datetime import timedelta
import aiohttp
from shapely.geometry import shape, Point
from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
import homeassistant.helpers.config_validation as cv
import voluptuous as vol

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=30)
DAYS_WITH_DETAILED_OUTLOOKS = 3

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_LATITUDE): cv.latitude,
    vol.Required(CONF_LONGITUDE): cv.longitude,
})


async def async_setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the NWS SPC Outlook sensor platform."""
    latitude = config[CONF_LATITUDE]
    longitude = config[CONF_LONGITUDE]

    coordinator = NWSSPCOutlookDataCoordinator(hass, latitude, longitude)
    await coordinator.async_config_entry_first_refresh()

    add_entities([NWSSPCOutlookSensor(coordinator, day) for day in range(1, 4)])


class NWSSPCOutlookSensor(Entity):
    """Representation of an SPC Outlook sensor for each day."""

    def __init__(self, coordinator, day):
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._day = day

    @property
    def name(self):
        """Return the name of the sensor."""
        return f"SPC Outlook Day {self._day}"

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._coordinator.data.get(f"cat_day{self._day}")

    @property
    def extra_state_attributes(self):
        """Return the additional attributes of the sensor."""
        return {
            "hail_probability": self._coordinator.data.get(f"hail_day{self._day}"),
            "wind_probability": self._coordinator.data.get(f"wind_day{self._day}"),
            "tornado_probability": self._coordinator.data.get(f"torn_day{self._day}")
        }

    async def async_update(self):
        """Update sensor using coordinator."""
        await self._coordinator.async_request_refresh()


class NWSSPCOutlookDataCoordinator(DataUpdateCoordinator):
    """Fetches data from the NWS API."""

    def __init__(self, hass, latitude, longitude):
        """Initialize."""
        super().__init__(hass, _LOGGER, name="NWS SPC Outlook", update_interval=SCAN_INTERVAL)
        self.latitude = latitude
        self.longitude = longitude

    async def _async_update_data(self):
        """Fetch data from the SPC API."""
        try:
            return await getspcoutlook(self.latitude, self.longitude)
        except Exception as error:
            raise UpdateFailed(f"Error fetching data: {error}") from error


async def getspcoutlook(latitude, longitude) -> dict:
    """Query SPC for the latest severe weather outlooks."""
    output = {}
    location = Point(longitude, latitude)

    async with aiohttp.ClientSession() as session:
        for day in range(1, 4):
            url = f"https://www.spc.noaa.gov/products/outlook/day{day}otlk_cat.lyr.geojson"
            result = False
            async with session.get(url, timeout=10) as resp:
                data = await resp.json()
                for feature in data["features"]:
                    polygon = shape(feature["geometry"])
                    if polygon.contains(location):
                        output[f"cat_day{day}"] = feature["properties"]["LABEL2"]
                        result = True

            if result and day <= DAYS_WITH_DETAILED_OUTLOOKS:
                for risk_type in ["torn", "hail", "wind"]:
                    risk_url = f"https://www.spc.noaa.gov/products/outlook/day{day}otlk_{risk_type}.lyr.geojson"
                    async with session.get(risk_url, timeout=10) as resp:
                        data = await resp.json()
                        for feature in data["features"]:
                            polygon = shape(feature["geometry"])
                            if polygon.contains(location):
                                output[f"{risk_type}_day{day}"] = feature["properties"]["LABEL2"]

    return output