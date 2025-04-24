"""
Config flow for NWS SPC Outlook integration.

This module defines the configuration and options flow used to set up
and customize the integration via the Home Assistant UI.
"""

from typing import Any

import homeassistant.helpers.config_validation as cv
import voluptuous as vol
from homeassistant import config_entries

from .const import CONF_LATITUDE, CONF_LONGITUDE, DOMAIN

# Valid latitude and longitude bounds
LAT_MIN = -90.0
LAT_MAX = 90.0
LON_MIN = -180.0
LON_MAX = 180.0

# Error messages
ERR_INVALID_COORDS = "Latitude or Longitude out of range"


def validate_coordinates(lat: float, lon: float) -> None:
    """
    Raise ValueError if coordinates are out of valid bounds.

    Args:
        lat: Latitude in decimal degrees.
        lon: Longitude in decimal degrees.

    Raises:
        ValueError: If latitude or longitude are outside valid ranges.

    """
    if not (LAT_MIN <= lat <= LAT_MAX and LON_MIN <= lon <= LON_MAX):
        raise ValueError(ERR_INVALID_COORDS)


class NWSSPCOutlookConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for setting up the NWS SPC Outlook integration."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """
        Handle the initial configuration step.

        Prompts user for latitude and longitude, validates inputs, and
        creates a configuration entry on success.

        Args:
            user_input: Dictionary of user-provided input from the form.

        Returns:
            A FlowResult indicating the next step in the configuration.

        """
        errors: dict[str, str] = {}

        if user_input is not None:
            try:
                lat = float(user_input[CONF_LATITUDE])
                lon = float(user_input[CONF_LONGITUDE])
                validate_coordinates(lat, lon)

                return self.async_create_entry(title="NWS SPC Outlook", data=user_input)
            except (ValueError, TypeError):
                errors["base"] = "invalid_coordinates"

        data_schema = vol.Schema(
            {
                vol.Required(CONF_LATITUDE): cv.latitude,
                vol.Required(CONF_LONGITUDE): cv.longitude,
            }
        )

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors,
        )


class NWSSPCOutlookOptionsFlow(config_entries.OptionsFlow):
    """Options flow for modifying settings after setup."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        """
        Initialize the options flow.

        Args:
            config_entry: Existing configuration entry for the integration.

        """
        self.config_entry = config_entry

    async def async_step_init(
        self, _user_input: dict[str, Any] | None = None
    ) -> config_entries.FlowResult:
        """
        Display the options menu.

        Returns:
            A FlowResult rendering the options form.

        """
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({}),
        )
