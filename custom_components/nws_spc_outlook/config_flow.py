"""Config flow for NWS SPC Outlook integration."""

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from typing import Any
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_LATITUDE, CONF_LONGITUDE

# Define constants for magic values
LAT_MIN = -90.0
LAT_MAX = 90.0
LON_MIN = -180.0
LON_MAX = 180.0


class NWS_SPCOutlookConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NWS SPC Outlook."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                lat = float(user_input[CONF_LATITUDE])
                lon = float(user_input[CONF_LONGITUDE])

                if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
                    raise ValueError("Latitude or Longitude out of range")

                return self.async_create_entry(title="NWS SPC Outlook", data=user_input)

            except (ValueError, TypeError):
                errors["base"] = "invalid_coordinates"

        data_schema = vol.Schema({
            vol.Required(CONF_LATITUDE): cv.latitude,
            vol.Required(CONF_LONGITUDE): cv.longitude,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        """Define the options flow for this component."""
        return NWS_SPCOutlookOptionsFlow(config_entry)


class NWS_SPCOutlookOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for NWS SPC Outlook."""

    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.config_entry = entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Handle the options step."""
        errors = {}

        if user_input is not None:
            try:
                lat = float(user_input[CONF_LATITUDE])
                lon = float(user_input[CONF_LONGITUDE])

                if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
                    raise ValueError("Latitude or Longitude out of range")

                # Save options
                return self.async_create_entry(title="", data=user_input)

            except ValueError:
                errors["base"] = "invalid_coordinates"

        # Define schema for options (allows changing coordinates)
        data_schema = vol.Schema({
            vol.Required(CONF_LATITUDE, default=self.config_entry.data.get(CONF_LATITUDE, 0.0)): cv.latitude,
            vol.Required(CONF_LONGITUDE, default=self.config_entry.data.get(CONF_LONGITUDE, 0.0)): cv.longitude,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
