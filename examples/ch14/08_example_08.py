# Розділ 14. Live API і генерація медіа – приклад 8 (рукопис: 14-live-media.md, рядок 382)
import asyncio
import random
from websockets.exceptions import ConnectionClosed
from google import genai
from google.genai import errors, types
from trembita.config import MODEL_LIVE


def driver_config(handle: str | None) -> types.LiveConnectConfig:
    return DRIVER_LOCKED.model_copy(update=dict(         # інструкція й інструменти – як у токені, підрозділ 14.4
        input_audio_transcription=types.AudioTranscriptionConfig(),
        output_audio_transcription=types.AudioTranscriptionConfig(),
        realtime_input_config=types.RealtimeInputConfig(
            automatic_activity_detection=types.AutomaticActivityDetection(
                start_of_speech_sensitivity=types.StartSensitivity.START_SENSITIVITY_LOW,  # шум кабіни
                end_of_speech_sensitivity=types.EndSensitivity.END_SENSITIVITY_LOW,        # не поспішати
                silence_duration_ms=900)),
        session_resumption=types.SessionResumptionConfig(handle=handle),   # None – нова сесія
        context_window_compression=types.ContextWindowCompressionConfig(
            trigger_tokens=100_000, sliding_window=types.SlidingWindow(target_tokens=60_000)),
    ))


async def drive_session(get_token, run_dialog, max_delay: float = 30.0) -> None:
    """get_token() – новий ефемерний токен від бекенду; run_dialog(session, state) повертає
    "done" (водій завершив рейс) або "reconnect" (прийшов go_away)."""
    state, delay = {"handle": None}, 1.0
    while True:
        try:
            client = genai.Client(api_key=await get_token(), http_options={"api_version": "v1alpha"})
            async with client.aio.live.connect(model=MODEL_LIVE, config=driver_config(state["handle"])) as s:
                delay = 1.0                   # з'єднання встановлено – пауза знову мінімальна
                if await run_dialog(s, state) == "done":
                    return
                continue                      # go_away: одразу нове з'єднання з тим самим дескриптором
        except (OSError, ConnectionClosed, errors.ServerError):
            pass                              # мережа зникла або сервер недоступний
        await asyncio.sleep(delay + random.uniform(0, delay / 2))   # експоненційна пауза з джитером
        delay = min(delay * 2, max_delay)
