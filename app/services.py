# app/services.py

import httpx

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
)


async def fetch_weather(lat: float, lon: float) -> dict:
    """
    Fetch current weather data from Open-Meteo API.
    Returns the raw JSON response as a Python dict.
    Raises an exception if the API call fails.
    """
    url = OPEN_METEO_URL.format(lat=lat, lon=lon)

    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(url)
            response.raise_for_status()
            data = response.json()
            data["location"] = f"({lat}, {lon})"  # optional: add location info
            return data
    except httpx.RequestError as e:
        raise RuntimeError(f"Weather API request error: {e}")
    except httpx.HTTPStatusError as e:
        raise RuntimeError(f"Weather API HTTP error: {e}")
