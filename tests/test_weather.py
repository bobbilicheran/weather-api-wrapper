# app/tests/test_weather.py

import pytest
import httpx
from app.services import get_weather


class MockResponse:
    """Mocked httpx response object"""
    def __init__(self, json_data, status_code=200):
        self._json = json_data
        self.status_code = status_code

    def raise_for_status(self):
        if self.status_code != 200:
            raise httpx.HTTPStatusError("Error", request=None, response=None)

    def json(self):
        return self._json


@pytest.mark.asyncio
async def test_get_weather_success(monkeypatch):
    """Test successful weather API call with mock data"""

    async def mock_get(*args, **kwargs):
        return MockResponse({"current_weather": {"temperature": 25, "windspeed": 10}})

    # Patch httpx.AsyncClient.get
    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    result = await get_weather(43.7, -79.4)
    assert "current_weather" in result
    assert result["current_weather"]["temperature"] == 25
    assert result["current_weather"]["windspeed"] == 10


@pytest.mark.asyncio
async def test_get_weather_failure(monkeypatch):
    """Test failed weather API call raises exception"""

    async def mock_get(*args, **kwargs):
        return MockResponse({}, status_code=500)

    monkeypatch.setattr(httpx.AsyncClient, "get", mock_get)

    with pytest.raises(httpx.HTTPStatusError):
        await get_weather(43.7, -79.4)
