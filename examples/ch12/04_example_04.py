# Розділ 12. Заземлення та вбудовані інструменти – приклад 4 (рукопис: 12-zazemlennia.md, рядок 149)
from google import genai
from google.genai import types

client = genai.Client()

url = "https://example-partner.eu/packaging-requirements"   # сторінка клієнта
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=f"Прочитай вимоги до пакування на {url}. Чи можемо ми прийняти "
             "палети 120×80 см висотою 1,8 м і вагою 900 кг? Відповідь обґрунтуй.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(url_context=types.UrlContext()),
               types.Tool(google_search=types.GoogleSearch())],  # пошук – для довідки
    ),
)
for m in resp.candidates[0].url_context_metadata.url_metadata or []:
    ok = m.url_retrieval_status == types.UrlRetrievalStatus.URL_RETRIEVAL_STATUS_SUCCESS
    print(m.retrieved_url, "прочитано" if ok else f"НЕ прочитано: {m.url_retrieval_status}")
print(resp.text)
