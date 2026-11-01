# Chapter 9. Thinking: Levels, Budgets and Thought Signatures – example 1 (manuscript: 09-myslennia.md, line 30)
from google import genai
from google.genai import types

client = genai.Client()

resp = client.models.generate_content(
    model="gemini-4-argon",
    contents="A load of 18 pallets of 420 kg each. A tractor unit carries 24 t, a semi-trailer has 33 pallet spaces. "
             "How many trips are needed for 70 pallets, and is one tractor unit enough for a day?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="medium"),
    ),
)
print(resp.text)
um = resp.usage_metadata
print("thoughts:", um.thoughts_token_count, "answer:", um.candidates_token_count)
