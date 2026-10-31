# Додаток Г. Довідник рецептів коду – приклад 22 (рукопис: 93-dodatok-g.md, рядок 422)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Які зміни для вантажівок на кордоні з Польщею діють цього місяця?",
    config=types.GenerateContentConfig(tools=[types.Tool(google_search=types.GoogleSearch())]),
)
meta = resp.candidates[0].grounding_metadata
if meta:
    print("запити:", meta.web_search_queries)
    for i, chunk in enumerate(meta.grounding_chunks or []):
        print(f"[{i + 1}] {chunk.web.title} ({chunk.web.uri})")
