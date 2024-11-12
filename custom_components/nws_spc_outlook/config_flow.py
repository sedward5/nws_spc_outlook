"""Config flow for NWS SPC Outlook integration."""
from typing import Any, Dict
import voluptuous as vol

from homeassistant import config_entries
from homeassistant.const import CONF_LATITUDE, CONF_LONGITUDE
from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from .const import DOMAIN  # Assuming you have DOMAIN defined as "nws_spc_outlook"


@config_entries.HANDLERS.register(DOMAIN)
class NWSOutlookConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for NWS SPC Outlook."""

    VERSION = 1

    async def async_step_user(self, user_input: Dict[str, Any] | None = None):
        """Handle the initial step."""
        errors = {}

        if user_input is not None:
            # Validate input (latitude and longitude are expected)
            try:
                lat = float(user_input[CONF_LATITUDE])
                lon = float(user_input[CONF_LONGITUDE])

                if not -90 <= lat <= 90 or not -180 <= lon <= 180:
                    raise ValueError("Latitude or Longitude out of range")

                # If input is valid, create an entry
                return self.async_create_entry(title="NWS SPC Outlook", data=user_input)

            except ValueError:
                errors["base"] = "invalid_coordinates"

        # Define form schema
        data_schema = vol.Schema({
            vol.Required(CONF_LATITUDE): cv.latitude,
            vol.Required(CONF_LONGITUDE): cv.longitude,
        })

        # Display form to the user with errors (if any)
        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Define the options flow for this component."""
        return NWSOutlookOptionsFlow(config_entry)


class NWSOutlookOptionsFlow(config_entries.OptionsFlow):
    """Handle options flow for NWS SPC Outlook."""

    def __init__(self, config_entry):
        """Initialize NWSOutlookOptionsFlow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        return await self.async_step_user()

    async def async_step_user(self, user_input=None):
        """Handle the options step."""
        errors = {}

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
            vol.Required(CONF_LATITUDE, default=self.config_entry.data[CONF_LATITUDE]): cv.latitude,
            vol.Required(CONF_LONGITUDE, default=self.config_entry.data[CONF_LONGITUDE]): cv.longitude,
        })

        return self.async_show_form(
            step_id="user", data_schema=data_schema, errors=errors
        )
