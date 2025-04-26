"""
Sensor for displaying NWS SPC Outlook data.

This module defines a sensor platform for Home Assistant that integrates
with the NOAA Storm Prediction Center (SPC) convective outlooks.

Each sensor represents a specific forecast day (Day 1-8) and exposes
categorical risk levels along with hazard-specific attributes (hail, wind,
tornado) for Days 1-2, and probabilistic outlooks for Days 4-8.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Final

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .coordinator import NWSSPCOutlookDataCoordinator

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddEntitiesCallback

_LOGGER = logging.getLogger(__name__)

DEFAULT_FILL: Final = "#000000"
DEFAULT_STROKE: Final = "#FFFFFF"


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """
    Set up SPC Outlook sensors dynamically.

    This creates one sensor for each day in the 8-day convective outlook.

    Args:
        hass: The Home Assistant instance.
        entry: Configuration entry for this integration.
        async_add_entities: Callback to register sensor entities.

    """
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

    sensors = [NWSSPCOutlookSensor(coordinator, day) for day in range(1, 9)]
    async_add_entities(sensors, update_before_add=True)


class NWSSPCOutlookSensor(
    CoordinatorEntity[NWSSPCOutlookDataCoordinator],
    SensorEntity,
):
    """
    Sensor for a specific day's SPC Outlook.

    Provides:
      - Categorical risk (e.g., Marginal, Slight) for Days 1-3
      - Hazard probabilities for Days 1-2 (hail, wind, tornado)
      - Probabilistic outlooks for Days 4-8

    """

    def __init__(self, coordinator: NWSSPCOutlookDataCoordinator, day: int) -> None:
        """
        Initialize the SPC Outlook sensor.

        Args:
            coordinator: Shared data coordinator instance.
            day: Forecast day number (1-8).

        """
        super().__init__(coordinator)
        self._day = day
        self._attr_name = f"SPC Outlook Day {day}"

    @property
    def name(self) -> str:
        """Name of the sensor (e.g., 'SPC Outlook Day 1')."""
        return f"SPC Outlook Day {self._day}"

    @property
    def state(self) -> str:
        """
        Main risk level for the forecast day.

        Returns:
            - For Days 1-3: Categorical outlook (e.g., 'Slight', 'Moderate').
            - For Days 4-8: Probabilistic outlook or 'No Risk'.

        """
        if self._day in range(1, 4):
            return self.coordinator.data.get(f"cat_day{self._day}", "No Risk")
        return self.coordinator.data.get(f"prob_day{self._day}", "No Risk")

    @property
    def extra_state_attributes(self) -> dict[str, str]:
        """
        Additional outlook data for this day.

        Includes:
          - Fill/stroke SVG values for outlook visualization
          - Hazard-specific probabilities for Days 1-2
          - Probabilistic styling for Days 4-8

        Returns:
            Dictionary of sensor attributes.

        """
        attributes: dict[str, str] = {}

        if self._day in range(1, 4):
            category_attrs = self.coordinator.data.get(
                f"cat_day{self._day}_attributes", {}
            )
            attributes.update(category_attrs)
            attributes["categorical_fill"] = category_attrs.get("fill", DEFAULT_FILL)
            attributes["categorical_stroke"] = category_attrs.get(
                "stroke", DEFAULT_STROKE
            )
        else:
            prob_attrs = self.coordinator.data.get(
                f"prob_day{self._day}_attributes", {}
            )
            attributes["probabilistic_fill"] = prob_attrs.get("fill", DEFAULT_FILL)
            attributes["probabilistic_stroke"] = prob_attrs.get(
                "stroke", DEFAULT_STROKE
            )

        if self._day in (1, 2):
            for risk_type in ("hail", "wind", "torn"):
                risk_key = f"{risk_type}_day{self._day}"
                risk_attr_key = f"{risk_type}_day{self._day}_attributes"
                risk_attrs = self.coordinator.data.get(risk_attr_key, {})

                attributes[f"{risk_type}_probability"] = self.coordinator.data.get(
                    risk_key, "No Risk"
                )
                attributes[f"{risk_type}_fill"] = risk_attrs.get("fill", DEFAULT_FILL)
                attributes[f"{risk_type}_stroke"] = risk_attrs.get(
                    "stroke", DEFAULT_STROKE
                )

        return attributes
