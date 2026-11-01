# Appendix D. Code Recipes – example 11 (manuscript: 93-appendix-d.md, line 184)
cfg = types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_level="high"))
history = [types.Content(role="user", parts=[types.Part(text="Route Lviv – Vienna: Chop or Krakovets?")])]
resp = client.models.generate_content(model="gemini-4-argon", contents=history, config=cfg)

history.append(resp.candidates[0].content)       # correct: all parts and signatures
# history.append(types.Content(role="model", parts=[types.Part(text=resp.text)]))  # signatures lost

history.append(types.Content(role="user", parts=[types.Part(text="And if the cargo is ADR?")]))
resp = client.models.generate_content(model="gemini-4-argon", contents=history, config=cfg)
