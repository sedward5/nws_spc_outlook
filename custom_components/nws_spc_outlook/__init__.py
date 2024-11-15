"""Initialize the NWS SPC Outlook integration."""
import logging

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, entry):
    """Set up nws_spc_outlook from a config entry."""
    _LOGGER.debug("Setting up NWS SPC Outlook integration entry")
    return True
