"""Implements unit tests for sensor.py."""

import pytest
import pytest_asyncio

from unittest.mock import AsyncMock, patch
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from custom_components.nws_spc_outlook.api import getspcoutlook
from custom_components.nws_spc_outlook.coordinator import NWSSPCOutlookDataCoordinator

LATITUDE = 35.0
LONGITUDE = -97.0
MOCK_API_RESPONSE = {"features": [{"properties": {"risk": "Slight"}}]}

@pytest_asyncio.fixture
async def hass_instance(tmp_path, event_loop) -> HomeAssistant:
    """Provide a properly initialized HomeAssistant instance."""
    hass = HomeAssistant(config_dir=str(tmp_path))
    await hass.async_start()
    yield hass
    await hass.async_stop()

@pytest_asyncio.fixture
async def coordinator(hass_instance) -> NWSSPCOutlookDataCoordinator:
    """Fixture for setting up NWSSPCOutlookDataCoordinator with mock data."""
    with patch(
        "custom_components.nws_spc_outlook.api.getspcoutlook",
        AsyncMock(return_value=MOCK_API_RESPONSE["features"][0]["properties"]),
    ):
        coordinator = NWSSPCOutlookDataCoordinator(hass_instance, LATITUDE, LONGITUDE)
        return coordinator

@pytest.mark.asyncio
async def test_getspcoutlook(hass_instance):
    session = async_get_clientsession(hass_instance)
    
    with patch(
        "custom_components.nws_spc_outlook.api.getspcoutlook",
        new_callable=AsyncMock
    ) as mock_get:
        mock_get.return_value = MOCK_API_RESPONSE
        
        result = await getspcoutlook(LATITUDE, LONGITUDE, session)
        
        assert result == MOCK_API_RESPONSE
