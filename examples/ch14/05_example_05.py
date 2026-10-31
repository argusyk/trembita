# Розділ 14. Live API і генерація медіа – приклад 5 (рукопис: 14-live-media.md, рядок 243)
import wave
from google import genai
from google.genai import types
from trembita.config import MODEL_TTS                  # gemini-3.8-flash-tts

client = genai.Client()


def voice(name: str) -> types.VoiceConfig:          # назва голосу – з переліку документації
    return types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=name))


ONE_VOICE = types.SpeechConfig(voice_config=voice("Kore"))
DIALOG = types.SpeechConfig(multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
    speaker_voice_configs=[types.SpeakerVoiceConfig(speaker="Ірина", voice_config=voice("Kore")),
                           types.SpeakerVoiceConfig(speaker="Водій", voice_config=voice("Puck"))]))

resp = client.models.generate_content(
    model=MODEL_TTS,
    contents="Скажи спокійно й чітко, як диктор: Увага водіям! На пункті пропуску Чоп "
             "черга близько двох годин. Плануйте запас часу.",
    config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=ONE_VOICE),
)
# для DIALOG: contents = "Озвуч діалог:\nІрина: Богдане, де ви зараз?\nВодій: Під Нижніми Воротами..."
pcm = resp.candidates[0].content.parts[0].inline_data.data
with wave.open("ogoloshennia.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)          # 16 біт
    wf.setframerate(24000)      # частота, вказана в документації для виходу TTS
    wf.writeframes(pcm)
