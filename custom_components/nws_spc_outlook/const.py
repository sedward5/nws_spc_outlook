"""
Constants for the NWS SPC Outlook integration.

This module defines configuration keys, default values, and API constants
used by the NWS SPC Outlook Home Assistant integration.
"""

DOMAIN = "nws_spc_outlook"
"""Integration domain identifier for Home Assistant."""

# Configuration keys for user-defined settings
CONF_LATITUDE = "latitude"
"""Config key for the latitude value defined in the integration settings."""

CONF_LONGITUDE = "longitude"
"""Config key for the longitude value defined in the integration settings."""

# Default values (used as fallbacks if no user input is provided)
DEFAULT_NAME = "NWS SPC Outlook"
"""Fallback name for the integration if no custom name is provided."""

DEFAULT_LATITUDE = 42.2808
"""Default latitude value (Ann Arbor, MI) used as a fallback location."""

DEFAULT_LONGITUDE = -83.7430
"""Default longitude value (Ann Arbor, MI) used as a fallback location."""

BASE_URL = "https://www.spc.noaa.gov/products/outlook"
"""Root URL for accessing SPC outlook products and data."""

DAYS_WITH_DETAILED_OUTLOOKS = 2
"""
Number of days (typically Day 1 and Day 2) with specific hazard 
details like hail, wind, and tornado risk.
"""
