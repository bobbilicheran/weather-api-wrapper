# app/llm.py

import os

try:
    import openai
except ImportError:
    openai = None  # Handle gracefully if OpenAI SDK not installed


def generate_weather_report(weather_json: dict) -> str:
    """
    Generate a human-readable weather report.
    Uses OpenAI if API key is set, otherwise returns a fallback message.
    """
    current = weather_json.get("current_weather", {})
    temp = current.get("temperature", "N/A")
    wind = current.get("windspeed", "N/A")

    # Fallback report (no LLM available)
    fallback = f"The temperature is {temp}°C with wind speed {wind} km/h."

    # If OpenAI is not available or no API key → return fallback
    api_key = os.getenv("OPENAI_API_KEY")
    if not openai or not api_key:
        return fallback

    try:
        openai.api_key = api_key
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"Write a short, friendly weather report for {temp}°C and wind {wind} km/h.",
            max_tokens=60,
            temperature=0.7,
        )
        return response.choices[0].text.strip()
    except Exception:
        return fallback
