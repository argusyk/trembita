# Chapter 14. The Live API and media generation – example 5 (manuscript: 14-live-media.md, line 243)
import wave
from google import genai
from google.genai import types
from trembita.config import MODEL_TTS                  # gemini-3.8-flash-tts

client = genai.Client()


def voice(name: str) -> types.VoiceConfig:          # the voice name comes from the documentation's list
    return types.VoiceConfig(prebuilt_voice_config=types.PrebuiltVoiceConfig(voice_name=name))


ONE_VOICE = types.SpeechConfig(voice_config=voice("Kore"))
DIALOG = types.SpeechConfig(multi_speaker_voice_config=types.MultiSpeakerVoiceConfig(
    speaker_voice_configs=[types.SpeakerVoiceConfig(speaker="Iryna", voice_config=voice("Kore")),
                           types.SpeakerVoiceConfig(speaker="Driver", voice_config=voice("Puck"))]))

resp = client.models.generate_content(
    model=MODEL_TTS,
    contents="Say it calmly and clearly, like an announcer: Attention, drivers! At the Chop border "
             "crossing the queue is about two hours. Allow extra time.",
    config=types.GenerateContentConfig(response_modalities=["AUDIO"], speech_config=ONE_VOICE),
)
# for DIALOG: contents = "Voice the dialogue:\nIryna: Bohdan, where are you now?\nDriver: Just below Nyzhni Vorota..."
pcm = resp.candidates[0].content.parts[0].inline_data.data
with wave.open("ogoloshennia.wav", "wb") as wf:
    wf.setnchannels(1)
    wf.setsampwidth(2)          # 16 bits
    wf.setframerate(24000)      # the rate given in the documentation for TTS output
    wf.writeframes(pcm)
