import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch
from custom_components.nws_spc_outlook.api import getspcoutlook
from custom_components.nws_spc_outlook.coordinator import NWSSPCOutlookDataCoordinator
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

MOCK_API_RESPONSE = {
    "features": [
        {"properties": {"outlook": "Severe", "confidence": "High"}}
    ]
}

@pytest_asyncio.fixture
async def hass_instance() -> HomeAssistant:
    """Provide a mock HomeAssistant instance."""
    hass = HomeAssistant()
    await hass.async_start()
    yield hass
    await hass.async_stop()

@pytest_asyncio.fixture
async def coordinator(hass_instance: HomeAssistant) -> NWSSPCOutlookDataCoordinator:
    """Fixture for setting up NWSSPCOutlookDataCoordinator with mock data."""
    with patch("custom_components.nws_spc_outlook.api.getspcoutlook", AsyncMock(return_value=MOCK_API_RESPONSE["features"][0]["properties"])):
        coordinator = NWSSPCOutlookDataCoordinator(hass_instance, 35.0, -97.0)
        await coordinator.async_config_entry_first_refresh()
        yield coordinator

@pytest.mark.asyncio
async def test_getspcoutlook():
    """Test API response handling."""
    with patch("custom_components.nws_spc_outlook.api.getspcoutlook", AsyncMock(return_value=MOCK_API_RESPONSE)) as mock_get:
        result = await getspcoutlook()
        assert "features" in result
        assert result["features"][0]["properties"]["outlook"] == "Severe"
        mock_get.assert_awaited()

@pytest.mark.asyncio
async def test_update_failed(coordinator: NWSSPCOutlookDataCoordinator):
    """Test handling of failed data update."""
    with patch("custom_components.nws_spc_outlook.api.getspcoutlook", AsyncMock(side_effect=Exception("API failure"))):
        await coordinator._async_update_data()
        assert coordinator.last_update_success is False
