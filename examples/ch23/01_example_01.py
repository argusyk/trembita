# Розділ 23. Промислова експлуатація на Gemini Enterprise Agent Platform – приклад 1 (рукопис: 23-produkshn.md, рядок 71)
import os
from google import genai
from google.genai import types


def make_client() -> genai.Client:
    """Промисловий клієнт «Трембіти»: Agent Platform, тайм-аут, повтори в SDK."""
    retry = types.HttpRetryOptions(
        attempts=3,              # разом із першою спробою
        initial_delay=1.0,       # секунди
        max_delay=8.0,           # для чату довше чекати немає сенсу
        exp_base=2.0,
        jitter=1.0,
        http_status_codes=[408, 429, 500, 503, 504],
    )
    return genai.Client(
        vertexai=True,           # у SDK 2.x той самий прапорець зветься enterprise=True
        project=os.environ["GOOGLE_CLOUD_PROJECT"],
        location=os.environ.get("GOOGLE_CLOUD_LOCATION", "europe-west4"),
        http_options=types.HttpOptions(timeout=20_000, retry_options=retry),  # мілісекунди
    )
