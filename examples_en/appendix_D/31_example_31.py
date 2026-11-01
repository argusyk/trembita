# Appendix D. Code Recipes – example 31 (manuscript: 93-appendix-d.md, line 609)
import asyncio

CONFIG = types.LiveConnectConfig(
    response_modalities=["AUDIO"],
    system_instruction="You are Trembita, the voice assistant for Smereka's drivers.",
    output_audio_transcription=types.AudioTranscriptionConfig())

async def main() -> None:
    async with client.aio.live.connect(model="gemini-3.8-live", config=CONFIG) as session:
        await session.send_client_content(
            turns=types.Content(role="user", parts=[types.Part(text="Until what time is the warehouse open?")]),
            turn_complete=True)
        audio = bytearray()
        async for msg in session.receive():
            if msg.data:
                audio.extend(msg.data)
            sc = msg.server_content
            if sc and sc.output_transcription and sc.output_transcription.text:
                print(sc.output_transcription.text, end="")

asyncio.run(main())
