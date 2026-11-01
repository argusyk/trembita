# Appendix A. Laboratory Practicum – example 8 (manuscript: 90-appendix-a.md, line 397)
import wave
from google import genai
from google.genai import types

client = genai.Client()
voice = types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore"))
resp = client.models.generate_content(
    model="gemini-3.8-flash-tts",
    contents="Say calmly: Dear visitors! The museum is open until 18:00, the ticket office until 17:30.",
    config=types.GenerateContentConfig(response_modalities=["AUDIO"],
                                       speech_config=types.SpeechConfig(voice_config=voice)))
parts = resp.parts or []                      # empty if the request was blocked
if not parts or parts[0].inline_data is None:
    raise SystemExit(f"No audio: {resp.prompt_feedback}")
with wave.open("ogoloshennia.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(parts[0].inline_data.data)
