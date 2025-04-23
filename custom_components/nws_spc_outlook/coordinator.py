"""
Coordinator for fetching and updating SPC Outlook data.

This module defines the NWSSPCOutlookDataCoordinator, responsible for 
retrieving and updating severe weather outlook data from the NOAA SPC API.
"""

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .api import getspcoutlook

_LOGGER = logging.getLogger(__name__)


class NWSSPCOutlookDataCoordinator(DataUpdateCoordinator):
    """
    Manages retrieval and storage of SPC Outlook data.

    Coordinates periodic updates from the SPC API, using Home Assistant's 
    data update coordinator pattern to efficiently manage shared state.
    """

    def __init__(self, hass: HomeAssistant, latitude: float, longitude: float) -> None:
        """
        Create a new SPC Outlook coordinator.

        Args:
            hass: Home Assistant instance.
            latitude: Latitude for the forecast location.
            longitude: Longitude for the forecast location.

        """
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
        """
        Fetch latest outlook data from the SPC API.

        Returns:
            A dictionary of SPC forecast data including categories and risk types.

        """
        return await getspcoutlook(self.latitude, self.longitude, self.session)
