"""Tests for the NWS SPC Outlook sensor integration."""

from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from homeassistant.helpers.update_coordinator import UpdateFailed

from custom_components.nws_spc_outlook.sensor import (
    NWSSPCOutlookDataCoordinator,
    NWSSPCOutlookSensor,
    getspcoutlook,
)

LATITUDE = 42.0
LONGITUDE = -83.0
DAY1_DATA = {
    "cat_day1": "Slight",
    "hail_day1": "5%",
    "wind_day1": "15%",
    "torn_day1": "2%",
}
DAY2_DATA = {
    "cat_day2": "Marginal",
    "hail_day2": "5%",
    "wind_day2": "5%",
    "torn_day2": "2%",
}
DAY3_DATA = {
    "cat_day3": "General Thunder",
    "hail_day3": "0%",
    "wind_day3": "5%",
    "torn_day3": "0%",
}


@pytest.fixture
async def coordinator(hass: Any) -> NWSSPCOutlookDataCoordinator:
    """Fixture for setting up NWSSPCOutlookDataCoordinator."""
    with patch(
        "custom_components.nws_spc_outlook.sensor.getspcoutlook",
        return_value={**DAY1_DATA, **DAY2_DATA, **DAY3_DATA},
    ):
        coordinator = NWSSPCOutlookDataCoordinator(hass, LATITUDE, LONGITUDE)
        await coordinator.async_config_entry_first_refresh()
    return coordinator


@pytest.mark.asyncio
async def test_coordinator_fetch_data(
    coordinator: NWSSPCOutlookDataCoordinator,
) -> None:
    """Test data fetching in the coordinator."""
    assert coordinator.data["cat_day1"] == "Slight"
    assert coordinator.data["hail_day1"] == "5%"
    assert coordinator.data["wind_day1"] == "15%"
    assert coordinator.data["torn_day1"] == "2%"

    assert coordinator.data["cat_day2"] == "Marginal"
    assert coordinator.data["hail_day2"] == "5%"
    assert coordinator.data["wind_day2"] == "5%"
    assert coordinator.data["torn_day2"] == "2%"

    assert coordinator.data["cat_day3"] == "General Thunder"
    assert coordinator.data["hail_day3"] == "0%"
    assert coordinator.data["wind_day3"] == "5%"
    assert coordinator.data["torn_day3"] == "0%"


@pytest.mark.asyncio
async def test_sensor_properties(coordinator: NWSSPCOutlookDataCoordinator) -> None:
    """Test the NWSSPCOutlookSensor properties."""
    day1_sensor = NWSSPCOutlookSensor(coordinator, day=1)
    day2_sensor = NWSSPCOutlookSensor(coordinator, day=2)
    day3_sensor = NWSSPCOutlookSensor(coordinator, day=3)

    assert day1_sensor.name == "SPC Outlook Day 1"
    assert day1_sensor.state == "Slight"
    assert day1_sensor.extra_state_attributes == {
        "hail_probability": "5%",
        "wind_probability": "15%",
        "tornado_probability": "2%",
    }

    assert day2_sensor.name == "SPC Outlook Day 2"
    assert day2_sensor.state == "Marginal"
    assert day2_sensor.extra_state_attributes == {
        "hail_probability": "5%",
        "wind_probability": "5%",
        "tornado_probability": "2%",
    }

    assert day3_sensor.name == "SPC Outlook Day 3"
    assert day3_sensor.state == "General Thunder"
    assert day3_sensor.extra_state_attributes == {
        "hail_probability": "0%",
        "wind_probability": "5%",
        "tornado_probability": "0%",
    }


@pytest.mark.asyncio
async def test_update_failed(coordinator: NWSSPCOutlookDataCoordinator) -> None:
    """Test handling of UpdateFailed exception in the coordinator."""
    with (
        patch(
            "custom_components.nws_spc_outlook.sensor.getspcoutlook",
            side_effect=Exception("API error"),
        ),
        pytest.raises(UpdateFailed),
    ):
        await coordinator.async_request_refresh()


@pytest.mark.asyncio
async def test_getspcoutlook() -> None:
    """Test the getspcoutlook function with mock API data."""
    with patch("aiohttp.ClientSession.get", new_callable=AsyncMock) as mock_get:
        mock_resp = AsyncMock()
        mock_resp.json.return_value = {
            "features": [
                {
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [
                            [
                                [-83.1, 42.1],
                                [-83.1, 41.9],
                                [-82.9, 41.9],
                                [-82.9, 42.1],
                                [-83.1, 42.1],
                            ]
                        ],
                    },
                    "properties": {"LABEL2": "Slight"},
                }
            ]
        }
        mock_get.return_value = mock_resp

        result = await getspcoutlook(LATITUDE, LONGITUDE)
        assert result["cat_day1"] == "Slight"
