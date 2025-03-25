"""Config flow for NWS SPC Outlook integration."""

from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.core import callback

from .const import CONF_LATITUDE, CONF_LONGITUDE, DOMAIN

# Define constants for magic values
LAT_MIN = -90.0
LAT_MAX = 90.0
LON_MIN = -180.0
LON_MAX = 180.0


def validate_coordinates(lat: float, lon: float) -> None:
    """Validate latitude and longitude range."""
    if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
        error_msg = "Latitude or Longitude out of range"
        raise ValueError(error_msg)


class NWSSPCOutlookConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NWS SPC Outlook."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                lat = float(user_input[CONF_LATITUDE])
                lon = float(user_input[CONF_LONGITUDE])

                validate_coordinates(lat, lon)

                return self.async_create_entry(title="NWS SPC Outlook", data=user_input)

            except (ValueError, TypeError):
                errors["base"] = "invalid_coordinates"

        data_schema = vol.Schema({
            vol.Required(CONF_LATITUDE): cv.latitude,
            vol.Required(CONF_LONGITUDE): cv.longitude,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )


class NWSSPCOutlookOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for NWS SPC Outlook."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(
        self, _user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """Manage the options."""
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )