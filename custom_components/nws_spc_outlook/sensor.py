"""Sensor for displaying NWS SPC Outlook data."""

import logging

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import NWSSPCOutlookDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up SPC Outlook sensors dynamically."""
    if "nws_spc_outlook" not in hass.data:
        hass.data["nws_spc_outlook"] = {}

    if entry.entry_id not in hass.data["nws_spc_outlook"]:
        coordinator = NWSSPCOutlookDataCoordinator(
            hass, entry.data[CONF_LATITUDE], entry.data[CONF_LONGITUDE]
        )
        await coordinator.async_config_entry_first_refresh()
        hass.data["nws_spc_outlook"][entry.entry_id] = coordinator

    coordinator = hass.data["nws_spc_outlook"][entry.entry_id]
    sensors = [NWSSPCOutlookSensor(coordinator, day) for day in range(1, 4)]
    async_add_entities(sensors, update_before_add=True)


class NWSSPCOutlookSensor(CoordinatorEntity, SensorEntity):
    """Representation of an SPC Outlook sensor."""

    def __init__(self, coordinator: NWSSPCOutlookDataCoordinator, day: int) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._day = day
        self._attr_name = f"SPC Outlook Day {self._day}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"SPC Outlook Day {self._day}"

    @property
    def state(self) -> str:
        """Return state of sensor."""
        return self.coordinator.data.get(f"cat_day{self._day}", "No Risk")

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return additional attributes."""
        return {
            # General Outlook Timing
            "valid_time": self.coordinator.data.get(f"valid_day{self._day}", None),
            "issue_time": self.coordinator.data.get(f"issue_day{self._day}", None),
            "expire_time": self.coordinator.data.get(f"expire_day{self._day}", None),
    
            # General Risk for the Day
            "categorical_stroke": self.coordinator.data.get(f"cat_stroke_day{self._day}", None),
            "categorical_fill": self.coordinator.data.get(f"cat_fill_day{self._day}", None),
    
            # Hail Risk Styling
            "hail_stroke": self.coordinator.data.get(f"hail_stroke_day{self._day}", None),
            "hail_fill": self.coordinator.data.get(f"hail_fill_day{self._day}", None),
    
            # Wind Risk Styling
            "wind_stroke": self.coordinator.data.get(f"wind_stroke_day{self._day}", None),
            "wind_fill": self.coordinator.data.get(f"wind_fill_day{self._day}", None),
    
            # Tornado Risk Styling
            "tornado_stroke": self.coordinator.data.get(f"torn_stroke_day{self._day}", None),
            "tornado_fill": self.coordinator.data.get(f"torn_fill_day{self._day}", None),
    
            # General Polygon Styling for the Outlook
            "stroke": self.coordinator.data.get(f"stroke_day{self._day}", None),
            "fill": self.coordinator.data.get(f"fill_day{self._day}", None),
        }
