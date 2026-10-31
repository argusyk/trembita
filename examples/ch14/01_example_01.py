# Розділ 14. Live API і генерація медіа – приклад 1 (рукопис: 14-live-media.md, рядок 59)
import asyncio
from google import genai
from google.genai import types
from trembita.config import MODEL_LIVE

client = genai.Client()
CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    system_instruction="Ти – «Трембіта», голосовий помічник водіїв «Смереки». Відповідай коротко.",
    output_audio_transcription=types.AudioTranscriptionConfig(),   # текст того, що сказала модель
)


async def main() -> None:
    async with client.aio.live.connect(model=MODEL_LIVE, config=CONFIG) as session:
        await session.send_client_content(
            turns=types.Content(role="user", parts=[types.Part(text="До котрої працює склад в Ужгороді?")]),
            turn_complete=True,
        )
        audio = bytearray()
        async for msg in session.receive():          # один хід моделі
            if msg.data:
                audio.extend(msg.data)               # фрагменти PCM-аудіо
            sc = msg.server_content
            if sc and sc.output_transcription and sc.output_transcription.text:
                print(sc.output_transcription.text, end="")
        print(f"\nотримано {len(audio)} байтів аудіо")


asyncio.run(main())
