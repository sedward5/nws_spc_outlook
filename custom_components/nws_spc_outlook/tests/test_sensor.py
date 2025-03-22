"""Tests for the NWS SPC Outlook sensor integration."""

from unittest.mock import AsyncMock, patch
import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.nws_spc_outlook.coordinator import NWSSPCOutlookDataCoordinator
from custom_components.nws_spc_outlook.sensor import NWSSPCOutlookSensor
from custom_components.nws_spc_outlook.api import getspcoutlook

LATITUDE = 42.0
LONGITUDE = -83.0

MOCK_API_RESPONSE = {
    "features": [
        {
            "geometry": {
                "type": "Polygon",
                "coordinates": [
                    [[-83.1, 42.1], [-83.1, 41.9], [-82.9, 41.9], [-82.9, 42.1], [-83.1, 42.1]]
                ],
            },
            "properties": {
                "LABEL2": "Slight",
                "hail_day1": "5%",
                "wind_day1": "15%",
                "torn_day1": "2%",
                "cat_day2": "Marginal",
                "hail_day2": "5%",
                "wind_day2": "5%",
                "torn_day2": "2%",
                "cat_day3": "General Thunder",
                "hail_day3": "0%",
                "wind_day3": "5%",
                "torn_day3": "0%",
            },
        }
    ]
}

@pytest.fixture
async def coordinator(hass):
    """Fixture for setting up NWSSPCOutlookDataCoordinator."""
    with patch("custom_components.nws_spc_outlook.api.getspcoutlook", return_value=MOCK_API_RESPONSE["features"][0]["properties"]):
        coordinator = NWSSPCOutlookDataCoordinator(hass, LATITUDE, LONGITUDE)
        await coordinator.async_config_entry_first_refresh()
    return coordinator

@pytest.mark.asyncio
async def test_coordinator_fetch_data(coordinator):
    """Test data fetching in the coordinator."""
    assert coordinator.data["LABEL2"] == "Slight"
    assert coordinator.data["hail_day1"] == "5%"
    assert coordinator.data["wind_day1"] == "15%"
    assert coordinator.data["torn_day1"] == "2%"

@pytest.mark.asyncio
async def test_sensor_properties(coordinator):
    """Test the NWSSPCOutlookSensor properties."""
    sensor = NWSSPCOutlookSensor(coordinator, day=1)
    
    assert sensor.name == "SPC Outlook Day 1"
    assert sensor.state == "Slight"
    assert sensor.extra_state_attributes == {
        "hail_probability": "5%",
        "wind_probability": "15%",
        "tornado_probability": "2%",
    }

@pytest.mark.asyncio
async def test_update_failed(hass):
    """Test handling of UpdateFailed exception in the coordinator."""
    with patch("custom_components.nws_spc_outlook.api.getspcoutlook", side_effect=Exception("API error")):
        coordinator = NWSSPCOutlookDataCoordinator(hass, LATITUDE, LONGITUDE)
        with pytest.raises(UpdateFailed):
            await coordinator.async_config_entry_first_refresh()

@pytest.mark.asyncio
async def test_getspcoutlook():
    """Test the getspcoutlook function with mock API data."""
    with patch("aiohttp.ClientSession.get", new_callable=AsyncMock) as mock_get:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = MOCK_API_RESPONSE
        mock_get.return_value.__aenter__.return_value = mock_resp

        result = await getspcoutlook(LATITUDE, LONGITUDE)
        assert result["LABEL2"] == "Slight"
