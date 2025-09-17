# app/tests/test_llm.py

import os
import pytest
from app import llm


def test_generate_weather_report_with_openai(monkeypatch):
    """Test LLM report generator with OpenAI key (mocked OpenAI call)."""
    from app import llm

    weather_json = {"current_weather": {"temperature": 25, "windspeed": 12}}

    # Set fake API key
    monkeypatch.setenv("OPENAI_API_KEY", "fake-key")

    # Mock response
    class MockChatCompletion:
        def __init__(self):
            self.choices = [
                type("obj", (object,), {
                    "message": type("m", (object,), {"content": "It is sunny and warm."})()
                })()
            ]

    class MockClient:
        def __init__(self, api_key=None): pass
        class chat:
            class completions:
                @staticmethod
                def create(*args, **kwargs):
                    return MockChatCompletion()

    # Patch OpenAI client
    monkeypatch.setattr(llm, "OpenAI", lambda api_key=None: MockClient())

    report = llm.generate_weather_report(weather_json)
    assert "sunny and warm" in report
