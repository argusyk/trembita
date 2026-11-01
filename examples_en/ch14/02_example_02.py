# Chapter 14. The Live API and media generation – example 2 (manuscript: 14-live-media.md, line 102)
from google.genai import types


async def send_microphone(session, chunks) -> None:
    """chunks: an asynchronous source of 16-bit 16 kHz PCM fragments from the microphone."""
    async for chunk in chunks:
        await session.send_realtime_input(audio=types.Blob(data=chunk, mime_type="audio/pcm;rate=16000"))


async def play_answers(session, player) -> None:
    """player: a wrapper over the speaker with write() and clear() methods."""
    while True:                                   # receive() ends after every turn
        async for msg in session.receive():
            sc = msg.server_content
            if sc and sc.interrupted:
                player.clear()                    # the driver interrupted: silence the unfinished part
            if msg.data:
                player.write(msg.data)            # 24 kHz PCM from the model
            if sc and sc.input_transcription and sc.input_transcription.text:
                print("Driver:", sc.input_transcription.text)
