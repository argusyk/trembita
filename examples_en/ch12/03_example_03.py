# Chapter 12. Grounding and Built-in Tools – example 3 (manuscript: 12-zazemlennia.md, line 117)
from google import genai
from google.genai import types

client = genai.Client()

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="The driver is near Chop right now. Find 2–3 guarded truck parking areas "
             "within a 30 km radius, with opening hours. Answer briefly.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_maps=types.GoogleMaps())],
        tool_config=types.ToolConfig(
            retrieval_config=types.RetrievalConfig(
                lat_lng=types.LatLng(latitude=48.43, longitude=22.21),  # Chop
                language_code="uk",
            ),
        ),
    ),
)
print(resp.text)
meta = resp.candidates[0].grounding_metadata
if meta:                                         # the model may not have used the maps
    for chunk in meta.grounding_chunks or []:
        if chunk.maps:
            print(chunk.maps.title, chunk.maps.uri)   # link to the place card
