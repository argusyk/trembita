# Appendix D. Code Recipes – example 22 (manuscript: 93-appendix-d.md, line 426)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="What changes for trucks at the border with Poland are in effect this month?",
    config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())]),
)
meta = resp.candidates[0].grounding_metadata if resp.candidates else None
if meta:
    print("queries:", meta.web_search_queries)
    for i, chunk in enumerate(meta.grounding_chunks or []):
        if chunk.web:
            print(f"[{i + 1}] {chunk.web.title} ({chunk.web.uri})")
