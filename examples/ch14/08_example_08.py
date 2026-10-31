# Розділ 14. Live API і генерація медіа – приклад 8 (рукопис: 14-live-media.md, рядок 361)
import asyncio
from websockets.exceptions import ConnectionClosed
from google import genai
from google.genai import types
from trembita.config import MODEL_LIVE


def driver_config(handle: str | None) -> types.LiveConnectConfig:
    return types.LiveConnectConfig(
        response_modalities=["AUDIO"],
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
    )


async def drive_session(client: genai.Client, run_dialog) -> None:
    """run_dialog(session, state) – задачі мікрофона, відтворення й інструментів."""
    state = {"handle": None}
    while True:
        try:
            async with client.aio.live.connect(model=MODEL_LIVE, config=driver_config(state["handle"])) as s:
                await run_dialog(s, state)    # оновлює state["handle"] з session_resumption_update
        except (OSError, ConnectionClosed):
            pass                              # мережа зникла: чекаємо й пробуємо знову
        await asyncio.sleep(3)
