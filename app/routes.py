from fastapi import APIRouter, HTTPException, Query
from app.services import fetch_weather
from app.llm import generate_weather_report

router = APIRouter()

@router.get("/weather")
async def get_weather(
    lat: float = Query(..., ge=-90, le=90),
    lon: float = Query(..., ge=-180, le=180),
):
    """
    API endpoint: Fetch weather and return JSON with LLM-generated report.
    """
    try:
        weather_data = await fetch_weather(lat, lon)
        report = generate_weather_report(weather_data)
        return {
            "latitude": lat,
            "longitude": lon,
            "temperature": weather_data["current_weather"]["temperature"],
            "report": report,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
