# Chapter 14. The Live API and media generation – example 8 (manuscript: 14-live-media.md, line 382)
import asyncio
import random
from websockets.exceptions import ConnectionClosed
from google import genai
from google.genai import errors, types
from trembita.config import MODEL_LIVE


def driver_config(handle: str | None) -> types.LiveConnectConfig:
    return DRIVER_LOCKED.model_copy(update=dict(         # instruction and tools as in the token, Section 14.4
        input_audio_transcription=types.AudioTranscriptionConfig(),
        output_audio_transcription=types.AudioTranscriptionConfig(),
        realtime_input_config=types.RealtimeInputConfig(
            automatic_activity_detection=types.AutomaticActivityDetection(
                start_of_speech_sensitivity=types.StartSensitivity.START_SENSITIVITY_LOW,  # cab noise
                end_of_speech_sensitivity=types.EndSensitivity.END_SENSITIVITY_LOW,        # do not hurry
                silence_duration_ms=900)),
        session_resumption=types.SessionResumptionConfig(handle=handle),   # None means a new session
        context_window_compression=types.ContextWindowCompressionConfig(
            trigger_tokens=100_000, sliding_window=types.SlidingWindow(target_tokens=60_000)),
    ))


async def drive_session(get_token, run_dialog, max_delay: float = 30.0) -> None:
    """get_token() returns a new ephemeral token from the backend; run_dialog(session, state) returns
    "done" (the driver has finished the trip) or "reconnect" (go_away has arrived)."""
    state, delay = {"handle": None}, 1.0
    while True:
        try:
            client = genai.Client(api_key=await get_token(), http_options={"api_version": "v1alpha"})
            async with client.aio.live.connect(model=MODEL_LIVE, config=driver_config(state["handle"])) as s:
                delay = 1.0                   # connection established: the pause is minimal again
                if await run_dialog(s, state) == "done":
                    return
                continue                      # go_away: a new connection right away with the same handle
        except (OSError, ConnectionClosed, errors.ServerError):
            pass                              # the network is gone or the server is unavailable
        await asyncio.sleep(delay + random.uniform(0, delay / 2))   # exponential pause with jitter
        delay = min(delay * 2, max_delay)
