# Розділ 14. Live API і генерація медіа – приклад 4 (рукопис: 14-live-media.md, рядок 185)
import datetime as dt
from google import genai
from google.genai import types
from trembita.config import MODEL_LIVE

client = genai.Client(http_options={"api_version": "v1alpha"})   # справжній ключ – лише на бекенді
DRIVER_INSTRUCTION = "Ти – «Трембіта», голосовий помічник водіїв «Смереки». Відповідай коротко."


def issue_driver_token(driver_id: str) -> str:
    """Викликається після входу водія в застосунок; driver_id перевіряє бекенд."""
    now = dt.datetime.now(dt.timezone.utc)
    token = client.auth_tokens.create(config=types.CreateAuthTokenConfig(
        uses=1,                                              # одна сесія на токен
        expire_time=now + dt.timedelta(hours=2),             # тривалість рейсового відрізка
        new_session_expire_time=now + dt.timedelta(minutes=1),
        live_connect_constraints=types.LiveConnectConstraints(
            model=MODEL_LIVE,
            config=types.LiveConnectConfig(response_modalities=["AUDIO"],
                                           system_instruction=DRIVER_INSTRUCTION),
        ),
    ))
    return token.name                                        # це значення отримує застосунок
