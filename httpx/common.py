"""Shared HTTPX setup for the standalone examples."""

import os
from pathlib import Path

import httpx
from dotenv import load_dotenv

MODEL = "gpt-6-luna"
BASE_URL = "https://api.openai.com/v1"


def api_key() -> str:
    here = Path(__file__).resolve().parent
    for path in (here / ".env.local", here.parent / ".env.local"):
        if path.is_file():
            load_dotenv(path, override=False)
            break
    key = os.getenv("OPENAI_API_KEY")
    if not key:
        raise RuntimeError("Set OPENAI_API_KEY or create .env.local here or one directory up.")
    return key


def post(path: str, payload: dict) -> dict:
    with httpx.Client(timeout=30) as client:
        response = client.post(
            f"{BASE_URL}{path}",
            headers={"Authorization": f"Bearer {api_key()}"},
            json=payload,
        )
    response.raise_for_status()
    return response.json()
