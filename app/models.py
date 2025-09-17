# app/models.py

from pydantic import BaseModel, Field

class WeatherResponse(BaseModel):
    latitude: float = Field(..., description="Latitude of the location")
    longitude: float = Field(..., description="Longitude of the location")
    temperature: float | None = Field(None, description="Current temperature in Celsius")
    report: str = Field(..., description="LLM-generated human-readable weather report")

    class Config:
        schema_extra = {
            "example": {
                "latitude": 43.7,
                "longitude": -79.4,
                "temperature": 24.1,
                "report": "It’s a warm day in your area with temperatures around 24.0°C and winds near 7.0 km/h."
            }
        }
