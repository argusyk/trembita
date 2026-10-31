# Додаток А. Практикум – приклад 8 (рукопис: 90-dodatok-a.md, рядок 396)
import wave
from google import genai
from google.genai import types

client = genai.Client()
voice = types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore"))
resp = client.models.generate_content(
    model="gemini-3.8-flash-tts",
    contents="Скажи спокійно: Шановні відвідувачі! Музей працює до 18:00, каса до 17:30.",
    config=types.GenerateContentConfig(response_modalities=["AUDIO"],
                                       speech_config=types.SpeechConfig(voice_config=voice)))
parts = resp.parts or []                      # порожньо, якщо запит заблоковано
if not parts or parts[0].inline_data is None:
    raise SystemExit(f"Аудіо немає: {resp.prompt_feedback}")
with wave.open("ogoloshennia.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(24000)
    wf.writeframes(parts[0].inline_data.data)
