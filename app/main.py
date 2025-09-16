# app/main.py

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.routes import router as weather_router

app = FastAPI(
    title="Weather API Wrapper",
    description="A wrapper around Open-Meteo API with LLM-generated weather reports.",
    version="1.0.0",
)

# Root health check
@app.get("/")
async def root():
    return {"message": "Weather API Wrapper is running. Go to /weather"}

# Mount frontend folder
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Include weather routes
app.include_router(weather_router)
