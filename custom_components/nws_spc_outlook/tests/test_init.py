"""Unit tests for the NWS SPC Outlook integration initialization."""

import pytest
import pytest_asyncio
from unittest.mock import AsyncMock, patch

from homeassistant.config_entries import ConfigEntries, ConfigEntry, SOURCE_USER
from homeassistant.const import CONF_LATITUDE
from homeassistant.core import HomeAssistant

from custom_components.nws_spc_outlook import async_setup_entry, async_unload_entry
from custom_components.nws_spc_outlook.const import DOMAIN, CONF_LONGITUDE
from custom_components.nws_spc_outlook.coordinator import NWSSPCOutlookDataCoordinator

LATITUDE = 35.0
LONGITUDE = -97.0
ENTRY_ID = "test_entry"


@pytest_asyncio.fixture
async def hass_instance(tmp_path) -> HomeAssistant:
    """Provide a properly initialized HomeAssistant instance."""
    hass = HomeAssistant(config_dir=str(tmp_path))
    hass.config_entries = ConfigEntries(hass)  # Initialize config_entries
    await hass.async_start()
    yield hass
    await hass.async_stop()


@pytest.fixture
def mock_config_entry():
    """Create a properly initialized ConfigEntry for testing."""
    return ConfigEntry(
        entry_id=ENTRY_ID,
        domain=DOMAIN,
        data={CONF_LATITUDE: LATITUDE, CONF_LONGITUDE: LONGITUDE},
        source=SOURCE_USER,
        title="NWS SPC Outlook",
        unique_id="test_unique_id",
        options={},
        version=1,
        minor_version=0,
        discovery_keys=None,
        subentries_data=None,
    )


@pytest.mark.asyncio
async def test_async_setup_entry(hass_instance, mock_config_entry):
    """Test setting up an entry successfully."""
    with patch(
        "custom_components.nws_spc_outlook.coordinator.NWSSPCOutlookDataCoordinator",
        autospec=True,
    ) as mock_coordinator_class:
        mock_coordinator = mock_coordinator_class.return_value
        mock_coordinator.async_config_entry_first_refresh = AsyncMock()

        with patch.object(
            hass_instance.config_entries, "async_forward_entry_setups", AsyncMock()
        ) as mock_forward:
            result = await async_setup_entry(hass_instance, mock_config_entry)

            assert result is True
            assert DOMAIN in hass_instance.data
            assert mock_config_entry.entry_id in hass_instance.data[DOMAIN]
            mock_coordinator.async_config_entry_first_refresh.assert_awaited_once()
            mock_forward.assert_awaited_once_with(mock_config_entry, ["sensor"])


@pytest.mark.asyncio
async def test_async_unload_entry(hass_instance, mock_config_entry):
    """Test unloading an entry successfully."""
    with patch(
        "custom_components.nws_spc_outlook.coordinator.NWSSPCOutlookDataCoordinator",
        autospec=True,
    ) as mock_coordinator_class:
        mock_coordinator = mock_coordinator_class.return_value
        mock_coordinator.async_unload = AsyncMock(return_value=True)

        hass_instance.data[DOMAIN] = {mock_config_entry.entry_id: mock_coordinator}

        with patch.object(
            hass_instance.config_entries, "async_unload_platforms", AsyncMock()
        ) as mock_unload_platforms:
            result = await async_unload_entry(hass_instance, mock_config_entry)

            assert result is True
            assert mock_config_entry.entry_id not in hass_instance.data[DOMAIN]
            mock_coordinator.async_unload.assert_awaited_once()
            mock_unload_platforms.assert_awaited_once_with(mock_config_entry, ["sensor"])
