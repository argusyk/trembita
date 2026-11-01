# Chapter 12. Grounding and Built-in Tools – example 4 (manuscript: 12-zazemlennia.md, line 161)
from google import genai
from google.genai import types

client = genai.Client()

url = "https://example-partner.eu/packaging-requirements"   # the customer's page
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=f"Read the packaging requirements at {url}. Can we accept "
             "120×80 cm pallets 1.8 m high and weighing 900 kg? Justify your answer.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(url_context=types.UrlContext()),
               types.Tool(google_search=types.GoogleSearch())],  # search – for reference
    ),
)
ucm = resp.candidates[0].url_context_metadata   # None if no page was read
for m in (ucm.url_metadata or []) if ucm else []:
    ok = m.url_retrieval_status == types.UrlRetrievalStatus.URL_RETRIEVAL_STATUS_SUCCESS
    print(m.retrieved_url, "read" if ok else f"NOT read: {m.url_retrieval_status}")
print(resp.text)
