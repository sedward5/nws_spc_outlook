"""Consts for NWS SPC Outlook."""
# const.py
DOMAIN = "nws_spc_outlook"

# Configuration keys
CONF_LATITUDE = "latitude"
CONF_LONGITUDE = "longitude"

# Defaults (optional, but helpful for fallback values)
DEFAULT_NAME = "NWS SPC Outlook"
DEFAULT_LATITUDE = 42.2808  # Approximate latitude for Ann Arbor, MI
DEFAULT_LONGITUDE = -83.7430  # Approximate longitude for Ann Arbor, MI

BASE_URL = "https://www.spc.noaa.gov/products/outlook"
DAYS_WITH_DETAILED_OUTLOOKS = 2
