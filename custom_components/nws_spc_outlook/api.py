"""NWS SPC API module for fetching severe weather outlook data.

This module handles communication with the Storm Prediction Center (SPC)
to retrieve severe weather outlooks in GeoJSON format. It determines
if a point falls within any forecast polygons and returns relevant data.
"""

import asyncio
import logging

import aiohttp
from shapely.geometry import Point, shape

from .const import BASE_URL, DAYS_WITH_DETAILED_OUTLOOKS

_LOGGER = logging.getLogger(__name__)

HTTP_OK = 200  # Avoid magic number


async def fetch_geojson(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch a GeoJSON file from the specified URL.

    Args:
        session: An aiohttp ClientSession for making the request.
        url: The URL to fetch the GeoJSON file from.

    Returns:
        A parsed JSON dictionary, or an empty dict on error.
    """
    try:
        headers = {"Accept": "application/json"}
        async with session.get(url, headers=headers, timeout=20) as resp:
            if resp.status != HTTP_OK:
                _LOGGER.error(
                    "Failed to fetch data from %s (HTTP %s)", url, resp.status
                )
                return {}

            text = await resp.text()
            if not text.strip():
                _LOGGER.exception("Empty response from %s", url)
                return {}

            try:
                return await resp.json(content_type=None)
            except (aiohttp.ContentTypeError, ValueError):
                _LOGGER.exception(
                    "Invalid JSON response from %s. Response body: %s", url, text[:500]
                )
                return {}

    except (aiohttp.ClientError, TimeoutError):
        _LOGGER.exception("Error fetching data from %s", url)
        return {}


async def getspcoutlook(
    latitude: float, longitude: float, session: aiohttp.ClientSession
) -> dict[str, str]:
    """Retrieve SPC severe weather outlooks for a given latitude and longitude.

    Queries the SPC API for categorical and detailed (tornado, hail, wind)
    outlooks, then determines which polygons, if any, contain the point.

    Args:
        latitude: Latitude of the location to check.
        longitude: Longitude of the location to check.
        session: An aiohttp ClientSession to reuse across requests.

    Returns:
        A dictionary containing matched outlook labels and metadata. Keys
        include outlook types like 'cat_day1' and additional attributes like
        'cat_day1_attributes'.
    """
    output: dict[str, str] = {}
    location = Point(longitude, latitude)

    # Add categorical outlooks for Days 1–8
    urls = {
        f"cat_day{day}": f"{BASE_URL}/day{day}otlk_cat.lyr.geojson"
        for day in range(1, 9)
    }

    # Add tornado, hail, and wind outlooks for configured days
    for day in range(1, DAYS_WITH_DETAILED_OUTLOOKS + 1):
        for risk_type in ["torn", "hail", "wind"]:
            urls[f"{risk_type}_day{day}"] = (
                f"{BASE_URL}/day{day}otlk_{risk_type}.lyr.geojson"
            )

    tasks = {key: fetch_geojson(session, url) for key, url in urls.items()}
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)

    for key, result in zip(tasks.keys(), results, strict=False):
        if isinstance(result, Exception):
            _LOGGER.exception("Failed to process %s due to %s", key, result)
            continue

        if not isinstance(result, dict):
            _LOGGER.error("Invalid data type for %s: %s", key, type(result))
            continue

        for feature in result.get("features", []):
            geometry = feature.get("geometry")
            if not geometry:
                _LOGGER.warning("Missing geometry in %s response", key)
                continue

            polygon = shape(geometry)
            if polygon.contains(location):
                output[key] = feature["properties"].get("LABEL2", "Unknown")
                output[f"{key}_attributes"] = {
                    "valid": feature["properties"].get("VALID", "Unknown"),
                    "issue": feature["properties"].get("ISSUE", "Unknown"),
                    "expire": feature["properties"].get("EXPIRE", "Unknown"),
                    "fill": feature["properties"].get("fill", "#000000"),
                    "stroke": feature["properties"].get("stroke", "#FFFFFF"),
                }

    return output
