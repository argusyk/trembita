# Розділ 14. Live API і генерація медіа – приклад 2 (рукопис: 14-live-media.md, рядок 102)
from google.genai import types


async def send_microphone(session, chunks) -> None:
    """chunks – асинхронне джерело фрагментів 16-бітного PCM 16 кГц з мікрофона."""
    async for chunk in chunks:
        await session.send_realtime_input(audio=types.Blob(data=chunk, mime_type="audio/pcm;rate=16000"))


async def play_answers(session, player) -> None:
    """player – обгортка над динаміком з методами write() і clear()."""
    while True:                                   # receive() завершується після кожного ходу
        async for msg in session.receive():
            sc = msg.server_content
            if sc and sc.interrupted:
                player.clear()                    # водій перебив: глушимо недоговорене
            if msg.data:
                player.write(msg.data)            # 24 кГц PCM від моделі
            if sc and sc.input_transcription and sc.input_transcription.text:
                print("Водій:", sc.input_transcription.text)
