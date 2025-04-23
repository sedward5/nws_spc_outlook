"""Initialize the NWS SPC Outlook integration.

This module sets up and manages the SPC Outlook integration within Home Assistant.
It handles configuration entry setup, creates and stores the coordinator, and
forwards entry setup to supported platforms.
"""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_LATITUDE, CONF_LONGITUDE, DOMAIN
from .coordinator import NWSSPCOutlookDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NWS SPC Outlook from a config entry.

    This function initializes the integration when a user adds it via the UI.
    It creates a data coordinator that fetches and updates data from the
    Storm Prediction Center (SPC) API, and sets up the sensor platform.

    Args:
        hass: The Home Assistant instance.
        entry: The configuration entry created from user input.

    Returns:
        True if setup was successful, False otherwise.
    """
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    coordinator = NWSSPCOutlookDataCoordinator(
        hass, entry.data[CONF_LATITUDE], entry.data[CONF_LONGITUDE]
    )

    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Forward setup to platform(s)
    await hass.config_entries.async_forward_entry_setups(entry, ["sensor"])

    # Ensure cleanup on unload
    entry.async_on_unload(lambda: async_unload_entry(hass, entry))

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload NWS SPC Outlook config entry.

    Cleans up resources when the integration is removed from Home Assistant.
    Unloads the sensor platform and removes the coordinator from memory.

    Args:
        hass: The Home Assistant instance.
        entry: The configuration entry to unload.

    Returns:
        True if unload was successful, False otherwise.
    """
    _LOGGER.debug("Unloading NWS SPC Outlook integration entry %s", entry.entry_id)

    if DOMAIN not in hass.data or entry.entry_id not in hass.data[DOMAIN]:
        return False

    coordinator = hass.data[DOMAIN].pop(entry.entry_id, None)

    if coordinator and hasattr(coordinator, "async_unload"):
        await coordinator.async_unload()

    # Remove DOMAIN key if no entries remain
    if not hass.data[DOMAIN]:
        hass.data.pop(DOMAIN)

    return await hass.config_entries.async_unload_platforms(entry, ["sensor"])
