"""Sensor for NWS SPC Outlook severe weather data integration in Home Assistant."""

import logging
from collections.abc import Callable
from datetime import timedelta
from typing import Any

import aiohttp
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from shapely.geometry import Point, shape

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=30)
DAYS_WITH_DETAILED_OUTLOOKS = 3

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_LATITUDE): cv.latitude,
        vol.Required(CONF_LONGITUDE): cv.longitude,
    }
)


async def async_setup_platform(
    hass: HomeAssistant,
    config: dict[str, Any],
    add_entities: Callable[[list[SensorEntity]], None],
    _discovery_info: Any = None,
) -> None:
    """Set up the NWS SPC Outlook sensor platform."""
    _LOGGER.debug("Setting up the NWS SPC Outlook sensor platform")
    latitude = config[CONF_LATITUDE]
    longitude = config[CONF_LONGITUDE]

    coordinator = NWSSPCOutlookDataCoordinator(hass, latitude, longitude)
    await coordinator.async_config_entry_first_refresh()

    sensors = [NWSSPCOutlookSensor(coordinator, day) for day in range(1, 4)]
    _LOGGER.debug(f"Sensors created: {sensors}")
    add_entities(sensors)


class NWSSPCOutlookSensor(SensorEntity):
    """Representation of an SPC Outlook sensor for each day."""

    def __init__(self, coordinator: "NWSSPCOutlookDataCoordinator", day: int) -> None:
        """Initialize the sensor."""
        self._coordinator = coordinator
        self._day = day

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"SPC Outlook Day {self._day}"

    @property
    def state(self) -> str:
        """Return the state of the sensor, defaulting to 'No Severe Weather' if no data is available."""
        return self._coordinator.data.get(f"cat_day{self._day}", "No Severe Weather")

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return additional attributes with default values for hail, wind, and tornado probability."""
        return {
            "hail_probability": self._coordinator.data.get(f"hail_day{self._day}", "No Data"),
            "wind_probability": self._coordinator.data.get(f"wind_day{self._day}", "No Data"),
            "tornado_probability": self._coordinator.data.get(f"torn_day{self._day}", "No Data"),
        }

    async def async_update(self) -> None:
        """Update sensor using coordinator."""
        await self._coordinator.async_request_refresh()


class NWSSPCOutlookDataCoordinator(DataUpdateCoordinator):
    """Fetches data from the NWS API."""

    def __init__(self, hass: HomeAssistant, latitude: float, longitude: float) -> None:
        """Initialize the data coordinator with placeholders to ensure entities are visible."""
        super().__init__(
            hass, _LOGGER, name="NWS SPC Outlook", update_interval=SCAN_INTERVAL
        )
        self.latitude = latitude
        self.longitude = longitude
        # Initialize default data to ensure entities always have data
        self.data: dict[str, str] = {
            f"cat_day{day}": "No Severe Weather" for day in range(1, 4)}
        self.data.update({f"{risk}_day{day}": "No Data" for day in range(
            1, 4) for risk in ["hail", "wind", "torn"]})

    async def _async_update_data(self) -> dict[str, str]:
        """Fetch data from the SPC API."""
        _LOGGER.debug("Attempting data update in NWSSPCOutlookDataCoordinator")
        try:
            return await self.hass.async_add_executor_job(
                getspcoutlook, self.latitude, self.longitude
            )
        except Exception as exc:
            error_message = "Error fetching SPC outlook data"
            raise UpdateFailed(error_message) from exc


async def getspcoutlook(latitude: float, longitude: float) -> dict[str, str]:
    """Query SPC for the latest severe weather outlooks."""
    output = {}
    location = Point(longitude, latitude)

    async with aiohttp.ClientSession() as session:
        for day in range(1, 4):
            url = f"https://www.spc.noaa.gov/products/outlook/day{
                day}otlk_cat.lyr.geojson"
            result = False
            async with session.get(url, timeout=10) as resp:
                data = await resp.json()
                for feature in data["features"]:
                    polygon = shape(feature["geometry"])
                    if polygon.contains(location):
                        output[f"cat_day{
                            day}"] = feature["properties"]["LABEL2"]
                        result = True

            if result and day <= DAYS_WITH_DETAILED_OUTLOOKS:
                for risk_type in ["torn", "hail", "wind"]:
                    risk_url = (
                        f"https://www.spc.noaa.gov/products/outlook/day{day}"
                        f"otlk_{risk_type}.lyr.geojson"
                    )
                    async with session.get(risk_url, timeout=10) as resp:
                        data = await resp.json()
                        for feature in data["features"]:
                            polygon = shape(feature["geometry"])
                            if polygon.contains(location):
                                output[f"{risk_type}_day{day}"] = feature["properties"][
                                    "LABEL2"
                                ]

    return output
