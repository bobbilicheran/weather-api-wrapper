# app/services.py

import httpx

OPEN_METEO_URL = (
    "https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&current_weather=true"
)

async def get_weather(lat: float, lon: float) -> dict:
    """
    Fetch current weather data from Open-Meteo API.
    Returns the raw JSON response as a Python dict.
    """
    url = OPEN_METEO_URL.format(lat=lat, lon=lon)

    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()
