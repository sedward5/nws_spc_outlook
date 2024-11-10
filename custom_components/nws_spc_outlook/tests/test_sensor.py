import pytest
from custom_components.nws_spc_outlook.sensor import NWSSPCOutlookSensor, NWSSPCOutlookDataCoordinator

@pytest.fixture
def coordinator(hass):
    return NWSSPCOutlookDataCoordinator(hass, 35.0, -97.0)

def test_sensor_initialization(coordinator):
    sensor = NWSSPCOutlookSensor(coordinator, 1)
    assert sensor.name == "SPC Outlook Day 1"

def test_sensor_update(coordinator):
    sensor = NWSSPCOutlookSensor(coordinator, 1)
    sensor.update()
    assert sensor.state == "15%"
    assert sensor.extra_state_attributes["hail_probability"] == "10%"
