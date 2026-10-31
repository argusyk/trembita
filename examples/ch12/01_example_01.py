# Розділ 12. Заземлення та вбудовані інструменти – приклад 1 (рукопис: 12-zazemlennia.md, рядок 42)
from google import genai
from google.genai import types

client = genai.Client()

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Які зміни в правилах перетину кордону Україна – Польща для вантажівок "
             "діють цього місяця? Відповідай стисло, з датами.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(google_search=types.GoogleSearch())],
    ),
)
print(resp.text)

meta = resp.candidates[0].grounding_metadata
if meta:                                         # модель могла й не шукати
    print("Запити:", meta.web_search_queries)
    for i, chunk in enumerate(meta.grounding_chunks or []):
        print(f"[{i + 1}] {chunk.web.title} – {chunk.web.domain}")
