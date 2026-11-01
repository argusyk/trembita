# Chapter 7. The Gemini API and the Google Gen AI SDK – example 2 (manuscript: 07-api.md, line 80)
from google import genai
from google.genai import types

client = genai.Client()

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="How much will it cost to ship 20 kg from Lviv to Kyiv?",
    config=types.GenerateContentConfig(
        system_instruction="You are Trembita, the assistant of the logistics company Smereka.",
        max_output_tokens=2048,               # ceiling for the response
        thinking_config=types.ThinkingConfig(thinking_level="low"),
        stop_sequences=["\n\n---"],           # where to force a stop
        seed=42,                              # for reproducible experiments
        labels={"team": "dispatch"},          # labels for cost reports
    ),
)
print(resp.text)
