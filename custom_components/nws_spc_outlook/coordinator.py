"""Coordinator for fetching and updating SPC Outlook data."""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import getspcoutlook

_LOGGER = logging.getLogger(__name__)


class NWSSPCOutlookDataCoordinator(DataUpdateCoordinator):
    """Coordinator to fetch and update SPC Outlook data."""

    def __init__(self, hass: HomeAssistant, latitude: float, longitude: float) -> None:
        """Initialize the coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            name="NWS SPC Outlook",
            update_interval=timedelta(minutes=30),
        )
        self.latitude = latitude
        self.longitude = longitude
        self.session = async_get_clientsession(hass)

    async def _async_update_data(self) -> dict:
        """Fetch the latest SPC Outlook data."""
        return await getspcoutlook(self.latitude, self.longitude, self.session)
