"""Sensor for fetching and displaying NWS SPC Outlook data."""
import logging
from collections.abc import Callable
from datetime import timedelta
from typing import Any

import aiohttp
import voluptuous as vol
from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant
from homeassistant.helpers import config_validation as cv
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity, DataUpdateCoordinator, UpdateFailed
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
    _LOGGER.debug("async_setup_platform called with config: %s", config)
    _LOGGER.debug("Entities being added: %s", sensors)
    _LOGGER.debug("Hass data for DOMAIN: %s", hass.data.get(DOMAIN))
    add_entities(sensors, True)
    
async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up SPC Outlook sensors dynamically."""
    coordinator = hass.data["nws_spc_outlook"][entry.entry_id]

    sensors = [NWSSPCOutlookSensor(coordinator, day) for day in range(1, 4)]
    async_add_entities(sensors, True)

class NWSSPCOutlookSensor(CoordinatorEntity, SensorEntity):
    """Representation of an SPC Outlook sensor for each day."""

    def __init__(self, coordinator: "NWSSPCOutlookDataCoordinator", day: int) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)  # Register entity with the update coordinator
        self._day = day
        self._attr_name = f"SPC Outlook Day {self._day}"  # Use HA’s built-in attribute

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"SPC Outlook Day {self._day}"

    @property
    def state(self) -> str:
        """Return state of sensor, default to 'No Severe Weather' if no data."""
        return self.coordinator.data.get(f"cat_day{self._day}", "No Severe Weather")

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return additional attributes with default values for hail/wind/tornado probabilities."""
        return {
            "hail_probability": 
                self.coordinator.data.get(f"hail_day{self._day}", "No Data"),
            "wind_probability": 
                self.coordinator.data.get(f"wind_day{self._day}", "No Data"),
            "tornado_probability": 
                self.coordinator.data.get(f"torn_day{self._day}", "No Data"),
        }

class NWSSPCOutlookDataCoordinator(DataUpdateCoordinator):
    """Fetches data from the NWS API."""

    def __init__(self, hass: HomeAssistant, latitude: float, longitude: float) -> None:
        """Initialize data coordinator w/placeholders to ensure entity visiblity."""
        super().__init__(
            hass,
            _LOGGER,
            name="NWS SPC Outlook",
            update_interval=SCAN_INTERVAL
        )
        self.latitude = latitude
        self.longitude = longitude
        # Initialize default data to ensure entities always have data
        self.data: dict[str, str] = {
            f"cat_day{day}": "No Severe Weather" for day in range(1, 4)
        }
        self.data.update({
            f"{risk}_day{day}":
                "No Data" for day in range(1, 4) for risk in ["hail", "wind", "torn"]
        })

    async def _async_update_data(self) -> dict[str, str]:
        """Fetch data from the SPC API."""
        _LOGGER.debug("Attempting data update in NWSSPCOutlookDataCoordinator")
        try:
            return await self.hass.async_add_executor_job(
                getspcoutlook, self.latitude, self.longitude
            )
        except Exception as exc:
            _LOGGER.error("Error fetching SPC outlook data: %s", exc)
            raise UpdateFailed("Error fetching SPC outlook data") from exc

async def getspcoutlook(latitude: float, longitude: float) -> dict[str, str]:
    """Query SPC for the latest severe weather outlooks."""
    output = {}
    location = Point(longitude, latitude)

    async with aiohttp.ClientSession() as session:
        for day in range(1, 4):
            url = f"https://www.spc.noaa.gov/products/outlook/day{day}otlk_cat.lyr.geojson"
            result = False
            async with session.get(url, timeout=10) as resp:
                if resp.status != 200:
                    _LOGGER.error("Failed to fetch SPC outlook data for Day %s", day)
                    continue
                data = await resp.json()
                for feature in data.get("features", []):
                    polygon = shape(feature["geometry"])
                    if polygon.contains(location):
                        output[f"cat_day{day}"] = feature["properties"].get("LABEL2", "Unknown")
                        result = True

            if result and day <= DAYS_WITH_DETAILED_OUTLOOKS:
                for risk_type in ["torn", "hail", "wind"]:
                    risk_url = f"https://www.spc.noaa.gov/products/outlook/day{day}otlk_{risk_type}.lyr.geojson"
                    async with session.get(risk_url, timeout=10) as resp:
                        if resp.status != 200:
                            _LOGGER.error("Failed to fetch %s data for Day %s", risk_type, day)
                            continue
                        data = await resp.json()
                        for feature in data.get("features", []):
                            polygon = shape(feature["geometry"])
                            if polygon.contains(location):
                                output[
                                    f"{risk_type}_day{day}"
                                ] = feature["properties"].get("LABEL2", "Unknown")

    return output
