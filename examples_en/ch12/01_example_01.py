# Chapter 12. Grounding and Built-in Tools – example 1 (manuscript: 12-zazemlennia.md, line 42)
from google import genai
from google.genai import types

client = genai.Client()

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="What changes to the Ukraine – Poland border crossing rules for trucks "
             "are in effect this month? Answer briefly, with dates.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
    ),
)
print(resp.text)

meta = resp.candidates[0].grounding_metadata
if meta:                                         # the model may not have searched
    print("Queries:", meta.web_search_queries)
    for i, chunk in enumerate(meta.grounding_chunks or []):
        if chunk.web:
            print(f"[{i + 1}] {chunk.web.title} – {chunk.web.domain}")
