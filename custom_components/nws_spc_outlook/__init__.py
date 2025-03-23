"""Initialize the NWS SPC Outlook integration."""

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_LATITUDE, CONF_LONGITUDE, DOMAIN
from .coordinator import NWSSPCOutlookDataCoordinator

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up NWS SPC Outlook from a config entry."""
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    # session = async_get_clientsession(hass)
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
    """Unload NWS SPC Outlook config entry."""
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
