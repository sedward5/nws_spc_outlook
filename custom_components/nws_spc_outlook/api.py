"""NWS SPC API module for fetching severe weather outlook data."""

import asyncio
import logging

import aiohttp
from shapely.geometry import Point, shape

from .const import BASE_URL, DAYS_WITH_DETAILED_OUTLOOKS

_LOGGER = logging.getLogger(__name__)

HTTP_OK = 200  # Replace magic number


async def fetch_geojson(session: aiohttp.ClientSession, url: str) -> dict:
    """
    Fetch SPC outlook data for a given latitude and longitude.

    This function queries the NWS SPC API, checks if the given location is inside
    any severe weather risk area, and returns the corresponding outlook data.
    """
    try:
        headers = {"Accept": "application/json"}  # Explicitly request JSON
        async with session.get(url, headers=headers, timeout=20) as resp:
            if resp.status != HTTP_OK:
                _LOGGER.error(
                    "Failed to fetch data from %s (HTTP %s)", url, resp.status
                )
                return {}

            text = await resp.text()  # Read response as text first
            if not text.strip():  # Handle empty response
                _LOGGER.exception("Empty response from %s", url)
                return {}

            try:
                return await resp.json(
                    content_type=None
                )  # Attempt to parse JSON directly
            except (aiohttp.ContentTypeError, ValueError):
                _LOGGER.exception(
                    "Invalid JSON response from %s. Response body: %s", url, text[:500]
                )
                return {}

    except (aiohttp.ClientError, TimeoutError):
        _LOGGER.exception("Error fetching data from %s", url)  # Remove unused variable
        return {}


async def getspcoutlook(
    latitude: float, longitude: float, session: aiohttp.ClientSession
) -> dict[str, str]:
    """Query SPC for the latest severe weather outlooks."""
    output = {}
    location = Point(longitude, latitude)

    urls = {
        f"cat_day{day}": f"{BASE_URL}/day{day}otlk_cat.lyr.geojson"
        for day in range(1, 4)
    }

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
                day_num = key.split("_")[-1]  # Extract day number

                # Extract risk label from LABEL2
                risk_label = feature["properties"].get("LABEL2", "Unknown")
                output[key] = risk_label

                # Map LABEL2 values to specific risk categories
                if key.startswith("cat_day"):
                    output[f"categorical_risk_day{day_num}"] = risk_label
                elif key.startswith("torn_day"):
                    output[f"tornado_probability_day{day_num}"] = risk_label
                elif key.startswith("hail_day"):
                    output[f"hail_probability_day{day_num}"] = risk_label
                elif key.startswith("wind_day"):
                    output[f"wind_probability_day{day_num}"] = risk_label

                # Extract stroke and fill colors
                stroke_key = f"{key}_stroke"
                fill_key = f"{key}_fill"
                output[stroke_key] = feature["properties"].get("stroke", None)
                output[fill_key] = feature["properties"].get("fill", None)

                # General stroke and fill for the day
                output[f"stroke_day{day_num}"] = feature["properties"].get("stroke", None)
                output[f"fill_day{day_num}"] = feature["properties"].get("fill", None)

    return output
    