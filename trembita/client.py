"""Надійний клієнт «Трембіти» (розділи 7 і 23): повторні спроби з затримкою та джитером."""
import random
import time

from google import genai
from google.genai import errors, types

from .config import MODEL_MAIN
from .prompts import SYSTEM_INSTRUCTION

RETRYABLE = {429, 500, 503, 504}


def make_client(**kwargs) -> genai.Client:
    """Клієнт Gemini API: ключ із GEMINI_API_KEY; vertexai=True – для Agent Platform."""
    return genai.Client(**kwargs)


def backoff_delays(attempts: int, base: float = 1.0, cap: float = 30.0, rng=random.random):
    """Затримки «повний джитер»: випадкове значення з [0, min(cap, base·2^k)]."""
    return [rng() * min(cap, base * 2 ** k) for k in range(attempts - 1)]


def with_retries(call, attempts: int = 5, sleep=time.sleep, delays=None):
    """Викликає call(), повторюючи на 429/5xx; інші помилки пропускає одразу."""
    delays = delays if delays is not None else backoff_delays(attempts)
    for k in range(attempts):
        try:
            return call()
        except errors.APIError as e:
            if e.code not in RETRYABLE or k == attempts - 1:
                raise
            sleep(delays[k])


def ask(question: str, *, model: str = MODEL_MAIN, client=None, thinking_level: str = "low") -> str:
    """Одне запитання – одна відповідь із системною інструкцією «Трембіти»."""
    client = client or make_client()
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        thinking_config=types.ThinkingConfig(thinking_level=thinking_level),
    )
    resp = with_retries(lambda: client.models.generate_content(model=model, contents=question, config=config))
    return resp.text or ""
