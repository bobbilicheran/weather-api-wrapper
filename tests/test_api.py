# app/tests/test_api.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_weather_success(monkeypatch):
    """Test /weather endpoint returns valid response with mock Open-Meteo."""

    async def mock_get_weather(lat, lon):
        return {"current_weather": {"temperature": 22, "windspeed": 8}}

    monkeypatch.setattr("app.services.get_weather", mock_get_weather)

    response = client.get("/weather?lat=43.7&lon=-79.4")
    assert response.status_code == 200

    data = response.json()
    assert data["latitude"] == 43.7
    assert data["longitude"] == -79.4
    assert data["temperature"] == 22
    assert "report" in data


def test_weather_invalid_lat():
    """Test /weather returns 422 for invalid latitude."""
    response = client.get("/weather?lat=200&lon=50")
    assert response.status_code == 422


def test_weather_service_failure(monkeypatch):
    """Test /weather returns 500 if Open-Meteo fails."""

    async def mock_get_weather(lat, lon):
        raise Exception("Mock API failure")

    monkeypatch.setattr("app.services.get_weather", mock_get_weather)

    response = client.get("/weather?lat=43.7&lon=-79.4")
    assert response.status_code == 500
    assert "Mock API failure" in response.text
