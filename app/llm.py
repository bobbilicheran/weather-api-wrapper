# app/llm.py

import os
import logging
from typing import Any

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None  # Gracefully handle if OpenAI SDK not installed

logger = logging.getLogger(__name__)


def generate_weather_report(weather_json: dict[str, Any]) -> str:
    """
    Generate a human-readable weather report.
    - If OPENAI_API_KEY is set and OpenAI is available → use GPT.
    - Otherwise → return a smart fallback report.
    """

    current = weather_json.get("current_weather", {})
    temp = current.get("temperature")
    wind = current.get("windspeed")
    cloud = current.get("cloudcover")
    humidity = current.get("humidity")
    location = weather_json.get("location", "your area")

    if temp is None:
        return "Weather data unavailable at the moment."

    # More granular classification
    if temp < 0:
        condition = "freezing cold"
    elif temp < 10:
        condition = "chilly"
    elif temp < 20:
        condition = "mild"
    elif temp < 30:
        condition = "warm"
    else:
        condition = "hot"

    fallback = (
        f"It’s a {condition} day in {location} with temperatures around {temp}°C"
        f" and winds near {wind} km/h."
    )

    # --- Try OpenAI if available ---
    api_key = os.getenv("OPENAI_API_KEY")
    if not OpenAI or not api_key:
        return fallback

    try:
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant that writes short, friendly weather reports."
                },
                {
                    "role": "user",
                    "content": f"Generate a weather report for {location}: {temp}°C, "
                               f"wind {wind} km/h, humidity {humidity}%, cloud cover {cloud}%."
                }
            ],
            max_tokens=60,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        logger.warning(f"[LLM Error] Falling back to smart report: {e}")
        return fallback
