import pytest
from app.services import fetch_weather


@pytest.mark.asyncio
async def test_fetch_weather_success(monkeypatch):
    async def mock_response(*args, **kwargs):
        class Mock:
            def raise_for_status(self): 
                return None
            def json(self): 
                return {"current_weather": {"temperature": 25, "windspeed": 10}}
        return Mock()

    monkeypatch.setattr("httpx.AsyncClient.get", mock_response)

    result = await fetch_weather(43.7, -79.4)
    assert result["current_weather"]["temperature"] == 25
