"""Initialize the NWS SPC Outlook integration."""
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN  # noqa: F401

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up nws_spc_outlook from a config entry."""
    _LOGGER.debug("Setting up NWS SPC Outlook integration entry")

    # Mark arguments as used to avoid linter errors
    _ = hass
    _ = entry

    return True
