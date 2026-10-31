# Розділ 12. Заземлення та вбудовані інструменти – приклад 3 (рукопис: 12-zazemlennia.md, рядок 107)
from google import genai
from google.genai import types

client = genai.Client()

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Водій зараз біля Чопа. Знайди 2–3 охоронювані стоянки для фур "
             "у радіусі 30 км, з годинами роботи. Відповідай стисло.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_maps=types.GoogleMaps())],
        tool_config=types.ToolConfig(
            retrieval_config=types.RetrievalConfig(
                lat_lng=types.LatLng(latitude=48.43, longitude=22.21),  # Чоп
                language_code="uk",
            ),
        ),
    ),
)
print(resp.text)
for chunk in resp.candidates[0].grounding_metadata.grounding_chunks or []:
    if chunk.maps:
        print(chunk.maps.title, chunk.maps.uri)   # посилання на картку місця
