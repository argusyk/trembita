# Chapter 9. Thinking: Levels, Budgets and Thought Signatures – example 5 (manuscript: 09-myslennia.md, line 173)
from google import genai
from google.genai import types

client = genai.Client()
cfg = types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_level="high"))
history = [types.Content(role="user", parts=[types.Part(text="Compare the Lviv–Vienna routes "
                                                         "via Chop and via Krakovets.")])]
resp = client.models.generate_content(model="gemini-4-argon", contents=history, config=cfg)

# Correct: append the model's content whole, with all parts and signatures
history.append(resp.candidates[0].content)

# Wrong: rebuild the turn from text, and the signatures are lost
# history.append(types.Content(role="model", parts=[types.Part(text=resp.text)]))

signed = [p for p in resp.candidates[0].content.parts if p.thought_signature]
print("parts with a signature:", len(signed))

history.append(types.Content(role="user", parts=[types.Part(text="And if the cargo is dangerous (ADR)?")]))
resp = client.models.generate_content(model="gemini-4-argon", contents=history, config=cfg)
