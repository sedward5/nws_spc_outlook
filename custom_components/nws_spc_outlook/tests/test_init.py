import pytest
from unittest.mock import AsyncMock, patch

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry

from custom_components.nws_spc_outlook.const import CONF_LATITUDE, CONF_LONGITUDE, DOMAIN
from custom_components.nws_spc_outlook import async_setup_entry, async_unload_entry
from custom_components.nws_spc_outlook.coordinator import NWSSPCOutlookDataCoordinator

@pytest.fixture
def hass():
    """Return a HomeAssistant instance."""
    return HomeAssistant()

@pytest.fixture
def config_entry():
    """Return a mock config entry."""
    return ConfigEntry(
        version=1,
        domain=DOMAIN,
        title="NWS SPC Outlook",
        data={CONF_LATITUDE: 35.0, CONF_LONGITUDE: -97.0},
        source="user",
        entry_id="test_entry_id",
    )

@pytest.fixture
def mock_coordinator():
    """Return a mock NWSSPCOutlookDataCoordinator."""
    return AsyncMock(spec=NWSSPCOutlookDataCoordinator)

@patch("custom_components.nws_spc_outlook.NWSSPCOutlookDataCoordinator", new_callable=AsyncMock)
async def test_async_setup_entry(mock_coordinator_class, hass, config_entry):
    """Test async_setup_entry initializes and sets up the integration."""
    mock_coordinator_instance = mock_coordinator_class.return_value
    mock_coordinator_instance.async_config_entry_first_refresh = AsyncMock()
    
    assert await async_setup_entry(hass, config_entry) is True
    
    # Ensure coordinator is stored in hass.data
    assert DOMAIN in hass.data
    assert config_entry.entry_id in hass.data[DOMAIN]
    
    # Ensure first refresh is called
    mock_coordinator_instance.async_config_entry_first_refresh.assert_awaited_once()

    # Ensure sensor platform is forwarded
    hass.config_entries.async_forward_entry_setups.assert_awaited_once_with(config_entry, ["sensor"])

@patch("custom_components.nws_spc_outlook.NWSSPCOutlookDataCoordinator", new_callable=AsyncMock)
async def test_async_unload_entry(mock_coordinator_class, hass, config_entry):
    """Test async_unload_entry properly cleans up the integration."""
    mock_coordinator_instance = mock_coordinator_class.return_value
    mock_coordinator_instance.async_unload = AsyncMock()
    
    # Manually add the entry to hass.data
    hass.data[DOMAIN] = {config_entry.entry_id: mock_coordinator_instance}
    
    assert await async_unload_entry(hass, config_entry) is True
    
    # Ensure entry is removed
    assert config_entry.entry_id not in hass.data[DOMAIN]
    
    # Ensure async_unload is called
    mock_coordinator_instance.async_unload.assert_awaited_once()

    # Ensure platform unloading is called
    hass.config_entries.async_unload_platforms.assert_awaited_once_with(config_entry, ["sensor"])
