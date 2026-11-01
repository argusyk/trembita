# Chapter 1. What Is Gemini: Google DeepMind, the Ecosystem and a Running Example – example 1 (manuscript: 01-vstup-gemini.md, line 181)
from google import genai
from google.genai import types

client = genai.Client()  # reads GEMINI_API_KEY from the environment

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="A customer asks: how many days does cargo take from Lviv to Warsaw?",
    config=types.GenerateContentConfig(
        system_instruction=(
            "You are Trembita, the assistant of the logistics company Smereka. "
            "Answer in Ukrainian, briefly and politely. "
            "If you do not have exact data, say so plainly."
        ),
        max_output_tokens=1024,
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
)
print(response.text)
