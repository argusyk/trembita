# Додаток Г. Довідник рецептів коду – приклад 24 (рукопис: 93-dodatok-g.md, рядок 464)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Знайди 2–3 охоронювані стоянки для фур у радіусі 30 км.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_maps=types.GoogleMaps())],
        tool_config=types.ToolConfig(retrieval_config=types.RetrievalConfig(
            lat_lng=types.LatLng(latitude=48.43, longitude=22.21), language_code="uk")),
    ),
)
meta = resp.candidates[0].grounding_metadata if resp.candidates else None
for chunk in (meta.grounding_chunks or []) if meta else []:
    if chunk.maps:
        print(chunk.maps.title, chunk.maps.uri)
