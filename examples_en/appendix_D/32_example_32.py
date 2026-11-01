# Appendix D. Code Recipes – example 32 (manuscript: 93-appendix-d.md, line 637)
import wave

speech = types.SpeechConfig(voice_config=types.VoiceConfig(
    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")))
resp = client.models.generate_content(
    model="gemini-3.8-flash-tts",
    contents="Say calmly: The queue at the Chop checkpoint is about two hours.",
    config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=speech),
)
content = resp.candidates[0].content if resp.candidates else None
part = content.parts[0] if content and content.parts else None
if part is None or part.inline_data is None:
    raise RuntimeError(f"No audio: {resp.prompt_feedback or 'empty response'}")
with wave.open("ogoloshennia.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)                           # 16 bits
    wf.setframerate(24000)
    wf.writeframes(part.inline_data.data)
