"""Config flow for NWS SPC Outlook integration."""
from typing import Any

import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant import config_entries
from homeassistant.core import callback

from .const import DOMAIN, CONF_LATITUDE, CONF_LONGITUDE


class NWS_SPC_OutlookConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NWS SPC Outlook."""

    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> config_entries.FlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                lat = float(user_input[CONF_LATITUDE])
                lon = float(user_input[CONF_LONGITUDE])

                if not (-90 <= lat <= 90 and -180 <= lon <= 180):
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
        return NWS_SPC_OutlookOptionsFlow(config_entry)


class NWS_SPC_OutlookOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for NWS SPC Outlook."""

    def __init__(self, entry: config_entries.ConfigEntry) -> None:
        """Initialize options flow."""
        self.entry_id = entry.entry_id  # Store only the entry_id

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> Any:
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> Any:
        """Handle the options step."""
        errors = {}
        config_entry = self.hass.config_entries.async_get_entry(self.entry_id)
        if config_entry is None:
            return self.async_abort(reason="config_entry_not_found")

        if user_input is not None:
            try:
                lat = float(user_input[CONF_LATITUDE])
                lon = float(user_input[CONF_LONGITUDE])

                if not -90 <= lat <= 90 or not -180 <= lon <= 180:
                    raise ValueError("Latitude or Longitude out of range")

                # Save options
                return self.async_create_entry(title="", data=user_input)

            except ValueError:
                errors["base"] = "invalid_coordinates"

        # Define schema for options (allows changing coordinates)
        data_schema = vol.Schema({
            vol.Required(CONF_LATITUDE, default=config_entry.data[CONF_LATITUDE]): cv.latitude,
            vol.Required(CONF_LONGITUDE, default=config_entry.data[CONF_LONGITUDE]): cv.longitude,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )