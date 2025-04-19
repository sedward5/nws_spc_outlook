"""Sensor for displaying NWS SPC Outlook data."""

from __future__ import annotations

import logging
from collections.abc import Callable
from typing import Final

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import NWSSPCOutlookDataCoordinator

_LOGGER = logging.getLogger(__name__)

DEFAULT_FILL: Final = "#000000"
DEFAULT_STROKE: Final = "#FFFFFF"


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    """Set up SPC Outlook sensors dynamically."""
    hass.data.setdefault("nws_spc_outlook", {})

    if entry.entry_id not in hass.data["nws_spc_outlook"]:
        coordinator = NWSSPCOutlookDataCoordinator(
            hass,
            entry.data[CONF_LATITUDE],
            entry.data[CONF_LONGITUDE],
        )
        await coordinator.async_config_entry_first_refresh()
        hass.data["nws_spc_outlook"][entry.entry_id] = coordinator

    coordinator = hass.data["nws_spc_outlook"][entry.entry_id]
    sensors = [NWSSPCOutlookSensor(coordinator, day) for day in range(1, 4)]
    async_add_entities(sensors, update_before_add=True)


class NWSSPCOutlookSensor(CoordinatorEntity[NWSSPCOutlookDataCoordinator], SensorEntity):
    """Representation of an SPC Outlook sensor."""

    def __init__(self, coordinator: NWSSPCOutlookDataCoordinator, day: int) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self._day = day
        self._attr_name = f"SPC Outlook Day {day}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return f"SPC Outlook Day {self._day}"

    @property
    def state(self) -> str:
        """Return the main outlook category for the day."""
        return self.coordinator.data.get(f"cat_day{self._day}", "No Risk")

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """Return additional attributes for display."""
        attributes: dict[str, str] = {}
        category_attrs = self.coordinator.data.get(f"cat_day{self._day}_attributes", {})

        attributes.update(category_attrs)
        attributes["categorical_fill"] = category_attrs.get("fill", DEFAULT_FILL)
        attributes["categorical_stroke"] = category_attrs.get("stroke", DEFAULT_STROKE)

        # Only Day 1 and 2 include specific risk types
        if self._day in (1, 2):
            for risk_type in ("hail", "wind", "torn"):
                risk_key = f"{risk_type}_day{self._day}"
                risk_attr_key = f"{risk_type}_day{self._day}_attributes"
                risk_attrs = self.coordinator.data.get(risk_attr_key, {})

                attributes[f"{risk_type}_probability"] = self.coordinator.data.get(
                    risk_key, "No Risk"
                )
                attributes[f"{risk_type}_fill"] = risk_attrs.get("fill", DEFAULT_FILL)
                attributes[f"{risk_type}_stroke"] = risk_attrs.get("stroke", DEFAULT_STROKE)

        return attributes
