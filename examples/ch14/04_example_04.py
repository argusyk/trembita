# Розділ 14. Live API і генерація медіа – приклад 4 (рукопис: 14-live-media.md, рядок 199)
import datetime as dt
from google import genai
from google.genai import types
from trembita.config import MODEL_LIVE
from trembita.tools import create_pickup, find_warehouse, track_shipment

client = genai.Client(http_options={"api_version": "v1alpha"})   # справжній ключ – лише на бекенді
DRIVER_INSTRUCTION = ("Ти – «Трембіта», голосовий помічник водіїв «Смереки». Відповідай коротко, "
                      "без переліків і розмітки; числа називай словами.")
DRIVER_LOCKED = types.LiveConnectConfig(                  # те, чого застосунок змінити не може
    response_modalities=["AUDIO"],
    system_instruction=DRIVER_INSTRUCTION,
    tools=[track_shipment, find_warehouse, create_pickup],  # SDK перетворить функції на оголошення
)


def issue_driver_token(driver_id: str) -> str:
    """Після входу водія і перед кожним перепідключенням; driver_id перевіряє бекенд."""
    now = dt.datetime.now(dt.timezone.utc)
    token = client.auth_tokens.create(config=types.CreateAuthTokenConfig(
        uses=1,                                              # одна нова сесія на токен
        expire_time=now + dt.timedelta(hours=2),             # тривалість рейсового відрізка
        new_session_expire_time=now + dt.timedelta(minutes=1),
        live_connect_constraints=types.LiveConnectConstraints(model=MODEL_LIVE, config=DRIVER_LOCKED),
        lock_additional_fields=[],                           # блокуємо лише поля, задані вище
    ))
    return token.name                                        # це значення отримує застосунок
