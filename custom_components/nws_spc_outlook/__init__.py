"""Initialize the NWS SPC Outlook integration."""
import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers import aiohttp_client

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NWS SPC Outlook from a config entry."""
    _LOGGER.debug("Setting up NWS SPC Outlook integration entry")

    # Store config entry data in hass.data
    hass.data.setdefault(DOMAIN, {})
    hass.data[DOMAIN] = entry.data

    # Initialize session for API calls if needed
    session = aiohttp_client.async_get_clientsession(hass)
    hass.data[DOMAIN]["session"] = session

    return True

async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload NWS SPC Outlook config entry."""
    _LOGGER.debug("Unloading NWS SPC Outlook integration entry")

    if DOMAIN in hass.data:
        del hass.data[DOMAIN]

    return True