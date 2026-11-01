# Appendix D. Code Recipes – example 25 (manuscript: 93-appendix-d.md, line 484)
url = "https://example-partner.eu/packaging-requirements"
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=f"Under the requirements at {url}, will 120×80 cm pallets 1.8 m high be accepted?",
    config=types.GenerateContentConfig(tools=[types.Tool(url_context=types.UrlContext())]),
)
ucm = resp.candidates[0].url_context_metadata if resp.candidates else None
for m in (ucm.url_metadata or []) if ucm else []:   # None – the tool was not called
    print(m.retrieved_url, m.url_retrieval_status)   # URL_RETRIEVAL_STATUS_SUCCESS?
