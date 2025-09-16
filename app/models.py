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
                "temperature": 22.1,
                "report": "It’s a mild day with calm winds. Great for outdoor activities!"
            }
        }
