import aiohttp
import asyncio
import logging
from shapely.geometry import shape, Point
from .const import BASE_URL, DAYS_WITH_DETAILED_OUTLOOKS

_LOGGER = logging.getLogger(__name__)

async def fetch_geojson(session: aiohttp.ClientSession, url: str) -> dict:
    """Fetch and return JSON data from an SPC endpoint, handling long responses and missing content types."""
    try:
        headers = {"Accept": "application/json"}  # Explicitly request JSON
        async with session.get(url, headers=headers, timeout=20) as resp:  # Increased timeout
            if resp.status != 200:
                _LOGGER.error("Failed to fetch data from %s (HTTP %s)", url, resp.status)
                return {}

            text = await resp.text()  # Read response as text first
            if not text.strip():  # Handle empty response
                _LOGGER.error("Empty response from %s", url)
                return {}

            try:
                return await resp.json()  # Attempt to parse JSON directly
            except (aiohttp.ContentTypeError, ValueError):  # Handle invalid JSON
                _LOGGER.error("Invalid JSON response from %s. Response body: %s", url, text[:500])
                return {}

    except (aiohttp.ClientError, asyncio.TimeoutError) as err:
        _LOGGER.error("Error fetching data from %s: %s", url, err)
        return {}

async def getspcoutlook(latitude: float, longitude: float, session: aiohttp.ClientSession) -> dict[str, str]:
    """Query SPC for the latest severe weather outlooks."""
    output = {}
    location = Point(longitude, latitude)

    urls = {f"cat_day{day}": f"{BASE_URL}/day{day}otlk_cat.lyr.geojson" for day in range(1, 4)}

    for day in range(1, DAYS_WITH_DETAILED_OUTLOOKS + 1):
        for risk_type in ["torn", "hail", "wind"]:
            urls[f"{risk_type}_day{day}"] = f"{BASE_URL}/day{day}otlk_{risk_type}.lyr.geojson"

    tasks = {key: fetch_geojson(session, url) for key, url in urls.items()}
    results = await asyncio.gather(*tasks.values(), return_exceptions=True)

    for key, result in zip(tasks.keys(), results):
        if isinstance(result, Exception):
            _LOGGER.error("Failed to process %s due to %s", key, result)
            continue
        if not isinstance(result, dict):  # Ensure we have a valid JSON response
            _LOGGER.error("Invalid data type for %s: %s", key, type(result))
            continue
        for feature in result.get("features", []):
            geometry = feature.get("geometry")
            if not geometry:  # Gracefully handle missing geometry
                _LOGGER.warning("Missing geometry in %s response", key)
                continue
            polygon = shape(geometry)
            if polygon.contains(location):
                output[key] = feature["properties"].get("LABEL2", "Unknown")

    return output
