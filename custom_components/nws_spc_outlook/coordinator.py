"""Coordinator for fetching and managing NWS SPC Outlook data."""
import logging
from datetime import timedelta
from typing import Any

import aiohttp
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed
from shapely.geometry import Point, shape

_LOGGER = logging.getLogger(__name__)

SCAN_INTERVAL = timedelta(minutes=30)
DAYS_WITH_DETAILED_OUTLOOKS = 3

class NWSSPCOutlookDataCoordinator(DataUpdateCoordinator):
    """Fetches and manages data from the NWS SPC API."""

    def __init__(self, hass: HomeAssistant, latitude: float, longitude: float) -> None:
        """Initialize data coordinator with default values."""
        super().__init__(
            hass,
            _LOGGER,
            name="NWS SPC Outlook",
            update_interval=SCAN_INTERVAL
        )
        self.latitude = latitude
        self.longitude = longitude
        self.data: dict[str, str] = {
            f"cat_day{day}": "No Severe Weather" for day in range(1, 4)
        }
        self.data.update({
            f"{risk}_day{day}": "No Data" for day in range(1, 4) for risk in ["hail", "wind", "torn"]
        })

    async def _async_update_data(self) -> dict[str, str]:
        """Fetch and process data from the SPC API."""
        _LOGGER.debug("Fetching SPC Outlook data...")
        url = "https://www.spc.noaa.gov/products/outlook/day1otlk.json"  # Example URL
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status != 200:
                        raise UpdateFailed(f"SPC API returned {response.status}")
                    data = await response.json()

            return self._process_spc_data(data)
        except Exception as err:
            raise UpdateFailed(f"Error fetching SPC data: {err}")

    def _process_spc_data(self, data: dict[str, Any]) -> dict[str, str]:
        """Process raw SPC data into structured format."""
        processed_data = {
            f"cat_day{day}": "No Severe Weather" for day in range(1, 4)
        }
        processed_data.update({
            f"{risk}_day{day}": "No Data" for day in range(1, 4) for risk in ["hail", "wind", "torn"]
        })

        for feature in data.get("features", []):
            properties = feature.get("properties", {})
            category = properties.get("category", "No Severe Weather")
            day = properties.get("day", 1)

            if 1 <= day <= 3:
                processed_data[f"cat_day{day}"] = category

        return processed_data