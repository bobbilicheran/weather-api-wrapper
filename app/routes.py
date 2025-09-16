# app/routes.py

from fastapi import APIRouter, Query, HTTPException
from app.services import get_weather
from app.llm import generate_weather_report
from app.models import WeatherResponse

router = APIRouter()

@router.get("/weather", response_model=WeatherResponse)
async def weather(
    lat: float = Query(..., description="Latitude of the location", ge=-90, le=90),
    lon: float = Query(..., description="Longitude of the location", ge=-180, le=180),
):
    """
    Fetch current weather data for the given coordinates
    and generate a human-readable weather report.
    """
    try:
        raw_weather = await get_weather(lat, lon)
        report = generate_weather_report(raw_weather)

        return WeatherResponse(
            latitude=lat,
            longitude=lon,
            temperature=raw_weather.get("current_weather", {}).get("temperature"),
            report=report,
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
