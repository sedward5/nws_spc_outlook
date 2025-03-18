"""Initialize the NWS SPC Outlook integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN, CONF_LATITUDE, CONF_LONGITUDE

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NWS SPC Outlook from a config entry."""
    # Ensure DOMAIN key exists and is mutable
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}
    # Ensure DOMAIN is initialized in hass.data
    hass.data.setdefault(DOMAIN, {})

    # Store session-related data per entry
    session = async_get_clientsession(hass)
    hass.data[DOMAIN][entry.entry_id] = {
        "latitude": entry.data[CONF_LATITUDE],
        "longitude": entry.data[CONF_LONGITUDE],
        "session": session,  # Store session if your integration needs one
    }

    # If your integration has platforms (like sensors), load them
    hass.config_entries.async_setup_platforms(entry, ["sensor"])

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload NWS SPC Outlook config entry."""
    _LOGGER.debug("Unloading NWS SPC Outlook integration entry %s", entry.entry_id)

    if DOMAIN in hass.data and entry.entry_id in hass.data[DOMAIN]:
        del hass.data[DOMAIN][entry.entry_id]

        # If no more entries exist, clean up DOMAIN key
        if not hass.data[DOMAIN]:
            del hass.data[DOMAIN]

    return True
