"""Sensor for NWS SPC Outlook severe weather data integration in Home Assistant."""

import logging
from datetime import timedelta
from typing import Any

import aiohttp
import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from shapely.geometry import Point, shape

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=30)
DAYS_WITH_DETAILED_OUTLOOKS = 3

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities) -> None:
    """Set up the NWS SPC Outlook sensor from a config entry."""
    _LOGGER.debug("Setting up SPC Outlook sensors from config entry")
    latitude = entry.data[CONF_LATITUDE]
    longitude = entry.data[CONF_LONGITUDE]
    
    session = async_get_clientsession(hass)
    coordinator = NWSSPCOutlookDataCoordinator(hass, session, latitude, longitude)
    
    await coordinator.async_config_entry_first_refresh()
    sensors = [NWSSPCOutlookSensor(coordinator, day) for day in range(1, 4)]
    async_add_entities(sensors, update_before_add=True)

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
        """Return the state of the sensor."""
        return self._coordinator.data.get(f"cat_day{self._day}", "No Severe Weather")

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return additional attributes."""
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

    def __init__(self, hass: HomeAssistant, session: aiohttp.ClientSession, latitude: float, longitude: float) -> None:
        """Initialize the data coordinator."""
        super().__init__(hass, _LOGGER, name="NWS SPC Outlook", update_interval=SCAN_INTERVAL)
        self.latitude = latitude
        self.longitude = longitude
        self.session = session
        self.data: dict[str, str] = {
            f"cat_day{day}": "No Severe Weather" for day in range(1, 4)
        }
        self.data.update({f"{risk}_day{day}": "No Data" for day in range(1, 4) for risk in ["hail", "wind", "torn"]})

    async def _async_update_data(self) -> dict[str, str]:
        """Fetch data from the SPC API."""
        _LOGGER.debug("Updating SPC Outlook data")
        try:
            return await getspcoutlook(self.session, self.latitude, self.longitude)
        except Exception as exc:
            raise UpdateFailed("Error fetching SPC outlook data") from exc

async def getspcoutlook(session: aiohttp.ClientSession, latitude: float, longitude: float) -> dict[str, str]:
    """Query SPC for the latest severe weather outlooks."""
    output = {}
    location = Point(longitude, latitude)

    for day in range(1, 4):
        try:
            url = f"https://www.spc.noaa.gov/products/outlook/day{day}otlk_cat.lyr.geojson"
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    _LOGGER.warning(f"Failed to fetch SPC data for day {day}, status {resp.status}")
                    continue
                
                data = await resp.json()
                if "features" not in data:
                    _LOGGER.warning(f"Invalid SPC response for day {day}: {data}")
                    continue

                result = False
                for feature in data["features"]:
                    polygon = shape(feature["geometry"])
                    if polygon.contains(location):
                        output[f"cat_day{day}"] = feature["properties"].get("LABEL2", "No Severe Weather")
                        result = True
                
                if not result:
                    output[f"cat_day{day}"] = "No Severe Weather"

            if day <= DAYS_WITH_DETAILED_OUTLOOKS:
                for risk_type in ["torn", "hail", "wind"]:
                    risk_url = f"https://www.spc.noaa.gov/products/outlook/day{day}otlk_{risk_type}.lyr.geojson"
                    async with session.get(risk_url, timeout=10) as resp:
                        if resp.status != 200:
                            _LOGGER.warning(f"Failed to fetch SPC risk data ({risk_type}) for day {day}")
                            continue
                        
                        data = await resp.json()
                        if "features" not in data:
                            _LOGGER.warning(f"Invalid SPC risk response ({risk_type}) for day {day}")
                            continue

                        for feature in data["features"]:
                            polygon = shape(feature["geometry"])
                            if polygon.contains(location):
                                output[f"{risk_type}_day{day}"] = feature["properties"].get("LABEL2", "No Data")

        except Exception as e:
            _LOGGER.error(f"Error fetching SPC outlook for day {day}: {e}")

    return output