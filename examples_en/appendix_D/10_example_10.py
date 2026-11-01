# Appendix D. Code Recipes – example 10 (manuscript: 93-appendix-d.md, line 166)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Departure from Lviv at 18:00, 270 km to Uzhhorod, speed limit 70 km/h, "
             "45 min rest after 4.5 h of driving. What is the earliest arrival time?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high", include_thoughts=True)),
)
content = resp.candidates[0].content if resp.candidates else None
for part in (content.parts or []) if content else []:
    if part.text:                            # a part may contain only a signature
        print("[thoughts]" if part.thought else "[answer]", part.text)
