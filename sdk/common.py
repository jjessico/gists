"""Shared setup for the standalone examples."""

import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

MODEL = "gpt-6-luna"


def client() -> OpenAI:
    # Prefer an already exported key; otherwise use the local file or the
    # parent directory's .env.local, where this project currently keeps it.
    here = Path(__file__).resolve().parent
    for path in (here / ".env.local", here.parent / ".env.local"):
        if path.is_file():
            load_dotenv(path, override=False)
            break
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("Set OPENAI_API_KEY or create .env.local here or one directory up.")
    return OpenAI()
