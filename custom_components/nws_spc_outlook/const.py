"""Constants for the NWS SPC Outlook integration."""

# Integration domain used to register the component in Home Assistant
DOMAIN = "nws_spc_outlook"

# Configuration keys for user-defined settings
CONF_LATITUDE = "latitude"  # User-specified latitude
CONF_LONGITUDE = "longitude"  # User-specified longitude

# Default values (used as fallbacks if no user input is provided)
DEFAULT_NAME = "NWS SPC Outlook"  # Default name for the integration
DEFAULT_LATITUDE = 42.2808  # Latitude for Ann Arbor, MI (example fallback location)
DEFAULT_LONGITUDE = -83.7430  # Longitude for Ann Arbor, MI (example fallback location)

# Base URL for the SPC outlook data
BASE_URL = "https://www.spc.noaa.gov/products/outlook"

# Number of days with detailed outlooks available (e.g., Day 1 and Day 2)
DAYS_WITH_DETAILED_OUTLOOKS = 2
