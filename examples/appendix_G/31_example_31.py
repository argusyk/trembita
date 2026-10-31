# Додаток Г. Довідник рецептів коду – приклад 31 (рукопис: 93-dodatok-g.md, рядок 598)
import asyncio

CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    system_instruction="Ти – «Трембіта», голосовий помічник водіїв «Смереки».",
    output_audio_transcription=types.AudioTranscriptionConfig())

async def main() -> None:
    async with client.aio.live.connect(model="gemini-3.8-live", config=CONFIG) as session:
        await session.send_client_content(
            turns=types.Content(role="user", parts=[types.Part(text="До котрої працює склад?")]),
            turn_complete=True)
        audio = bytearray()
        async for msg in session.receive():
            if msg.data:
                audio.extend(msg.data)
            sc = msg.server_content
            if sc and sc.output_transcription and sc.output_transcription.text:
                print(sc.output_transcription.text, end="")

asyncio.run(main())
