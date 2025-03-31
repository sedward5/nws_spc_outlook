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
        self.data = {}  # Store fetched data

    async def _async_update_data(self) -> dict:
        """Fetch the latest SPC Outlook data."""
        raw_data = await getspcoutlook(self.latitude, self.longitude, self.session)

        # Extract general attributes
        outlook_data = {
            "VALID": raw_data.get("VALID"),
            "ISSUE": raw_data.get("ISSUE"),
            "EXPIRE": raw_data.get("EXPIRE"),
        }

        # Extract categorical and risk-type attributes dynamically
        for day in range(1, 4):  # Assuming up to 3-day outlook
            outlook_data[f"categorical_day{day}"] = raw_data.get(f"cat_day{day}", "None")
            outlook_data[f"categorical_stroke_day{day}"] = raw_data.get(f"cat_day{day}_stroke")
            outlook_data[f"categorical_fill_day{day}"] = raw_data.get(f"cat_day{day}_fill")

            for risk in ["torn", "hail", "wind"]:
                outlook_data[f"{risk}_day{day}"] = raw_data.get(f"{risk}_day{day}", "None")
                outlook_data[f"{risk}_stroke_day{day}"] = raw_data.get(f"{risk}_day{day}_stroke")
                outlook_data[f"{risk}_fill_day{day}"] = raw_data.get(f"{risk}_day{day}_fill")

        self.data = outlook_data  # Store the structured data
        return outlook_data
