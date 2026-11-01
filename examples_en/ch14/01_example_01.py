# Chapter 14. The Live API and media generation – example 1 (manuscript: 14-live-media.md, line 59)
import asyncio
from google import genai
from google.genai import types
from trembita.config import MODEL_LIVE

client = genai.Client()
CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    system_instruction="You are Trembita, the voice assistant for Smereka's drivers. Answer briefly.",
    output_audio_transcription=types.AudioTranscriptionConfig(),   # text of what the model said
)


async def main() -> None:
    async with client.aio.live.connect(model=MODEL_LIVE, config=CONFIG) as session:
        await session.send_client_content(
            turns=types.Content(role="user", parts=[types.Part(text="What time does the Uzhhorod warehouse close?")]),
            turn_complete=True,
        )
        audio = bytearray()
        async for msg in session.receive():          # one model turn
            if msg.data:
                audio.extend(msg.data)               # fragments of PCM audio
            sc = msg.server_content
            if sc and sc.output_transcription and sc.output_transcription.text:
                print(sc.output_transcription.text, end="")
        print(f"\nreceived {len(audio)} bytes of audio")


asyncio.run(main())
