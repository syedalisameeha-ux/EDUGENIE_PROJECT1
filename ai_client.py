"""Shared Gemini client and response helpers."""
import os
from functools import lru_cache

from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()


@lru_cache(maxsize=1)
def get_client():
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is missing. Copy .env.example to .env and add an API key from Google AI Studio."
        )
    return genai.Client(api_key=api_key)


def generate_text(prompt: str, *, json_mode: bool = False) -> str:
    """Generate text using the configured Gemini model."""
    model = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    config = types.GenerateContentConfig(
        temperature=0.4,
        response_mime_type="application/json" if json_mode else "text/plain",
    )
    response = get_client().models.generate_content(
        model=model,
        contents=prompt,
        config=config,
    )
    result = (response.text or "").strip()
    if not result:
        raise RuntimeError("The AI provider returned an empty response. Please try again.")
    return result
