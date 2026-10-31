# Додаток Г. Довідник рецептів коду – приклад 32 (рукопис: 93-dodatok-g.md, рядок 637)
import wave

speech = types.SpeechConfig(voice_config=types.VoiceConfig(
    prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name="Kore")))
resp = client.models.generate_content(
    model="gemini-3.8-flash-tts",
    contents="Скажи спокійно: На пункті пропуску Чоп черга близько двох годин.",
    config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=speech),
)
content = resp.candidates[0].content if resp.candidates else None
part = content.parts[0] if content and content.parts else None
if part is None or part.inline_data is None:
    raise RuntimeError(f"Аудіо немає: {resp.prompt_feedback or 'порожня відповідь'}")
with wave.open("ogoloshennia.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)                           # 16 біт
    wf.setframerate(24000)
    wf.writeframes(part.inline_data.data)
