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
    
        if not raw_data or "features" not in raw_data or not raw_data["features"]:
            _LOGGER.error("No valid SPC Outlook data received")
            return {}
    
        # Extract properties from the first feature
        properties = raw_data["features"][0].get("properties", {})
    
        _LOGGER.debug("Extracted properties: %s", properties)
    
        # Initialize risk type mapping
        risk_mapping = {
            "tornado": "tornado_probability",
            "wind": "wind_probability",
            "hail": "hail_probability",
        }
    
        # Extract probability data from LABEL2
        probabilities = {
            "tornado_probability": None,
            "wind_probability": None,
            "hail_probability": None,
        }
        categorical_risk = None  # Default unknown risk level
    
        label2 = properties.get("LABEL2", "").lower()  # Normalize case
    
        for risk, attr in risk_mapping.items():
            if risk in label2:
                try:
                    probabilities[attr] = int(label2.split("%")[0])  # Extract numeric value
                except ValueError:
                    _LOGGER.warning("Unexpected LABEL2 format: %s", label2)
    
        # Determine categorical risk (LABEL)
        categorical_risk = properties.get("LABEL", "Unknown")
    
        # Construct outlook data dictionary
        outlook_data = {
            "VALID": properties.get("VALID", "Unknown"),
            "ISSUE": properties.get("ISSUE", "Unknown"),
            "EXPIRE": properties.get("EXPIRE", "Unknown"),
            "stroke": properties.get("stroke", "None"),
            "fill": properties.get("fill", "None"),
            "categorical_risk": categorical_risk,
            **probabilities,  # Merge probability mappings
        }
    
        _LOGGER.debug("Processed SPC Outlook data: %s", outlook_data)
    
        self.data = outlook_data
        return outlook_data
