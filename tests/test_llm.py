# app/tests/test_llm.py

import os
import pytest
from app import llm


def test_generate_weather_report_fallback(monkeypatch):
    """Test LLM report generator without OpenAI key (fallback mode)."""
    weather_json = {"current_weather": {"temperature": 20, "windspeed": 5}}

    # Ensure API key is not set
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    result = llm.generate_weather_report(weather_json)
    assert "20" in result  # Should include temperature
    assert "5" in result   # Should include windspeed


def test_generate_weather_report_with_openai(monkeypatch):
    """Test LLM report generator with OpenAI key (mocked OpenAI call)."""
    weather_json = {"current_weather": {"temperature": 25, "windspeed": 12}}

    # Set fake API key
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

    # Mock openai.Completion.create
    class MockResponse:
        choices = [type("obj", (object,), {"text": " It is sunny and warm."})()]

    def mock_create(*args, **kwargs):
        return MockResponse

    monkeypatch.setattr(llm.openai.Completion, "create", mock_create)

    result = llm.generate_weather_report(weather_json)
    assert "sunny" in result.lower()
    assert "warm" in result.lower()
