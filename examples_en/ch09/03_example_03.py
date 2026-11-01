# Chapter 9. Thinking: Levels, Budgets and Thought Signatures – example 3 (manuscript: 09-myslennia.md, line 110)
from google import genai
from google.genai import types

client = genai.Client()
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Shipment SM-2610-0388 left Lviv on Monday at 18:00. "
             "It is 270 km to Uzhhorod, the speed limit for trucks is 70 km/h, the driver must "
             "rest for 45 min after 4.5 h of driving. What is the earliest arrival time?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high",
                                             include_thoughts=True),
    ),
)
for part in resp.candidates[0].content.parts:
    if not part.text:
        continue                       # parts without text (for example, only a signature)
    if part.thought:
        print("[thought summary]\n", part.text)
    else:
        print("[answer]\n", part.text)
