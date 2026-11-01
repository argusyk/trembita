# Appendix D. Code Recipes – example 24 (manuscript: 93-appendix-d.md, line 464)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Find 2–3 guarded truck parking lots within a 30 km radius.",
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
