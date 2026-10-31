# Додаток Г. Довідник рецептів коду – приклад 25 (рукопис: 93-dodatok-g.md, рядок 477)
url = "https://example-partner.eu/packaging-requirements"
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=f"Чи приймуть за вимогами {url} палети 120×80 см висотою 1,8 м?",
    config=types.GenerateContentConfig(tools=[types.Tool(url_context=types.UrlContext())]),
)
for m in resp.candidates[0].url_context_metadata.url_metadata or []:
    print(m.retrieved_url, m.url_retrieval_status)   # URL_RETRIEVAL_STATUS_SUCCESS?
