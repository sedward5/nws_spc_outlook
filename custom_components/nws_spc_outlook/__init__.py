"""Initialize the NWS SPC Outlook integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NWS SPC Outlook from a config entry."""
    session = async_get_clientsession(hass)

    # Ensure DOMAIN exists in hass.data and is mutable
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    hass.data[DOMAIN]["session"] = session

    # Additional setup steps here...

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload NWS SPC Outlook config entry."""
    _LOGGER.debug("Unloading NWS SPC Outlook integration entry")

    if DOMAIN in hass.data:
        del hass.data[DOMAIN]

    return True