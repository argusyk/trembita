# Chapter 23. Production on Gemini Enterprise Agent Platform – example 3 (manuscript: 23-produkshn.md, line 150)
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_MAIN

client = make_client()
resp = client.models.generate_content(
    model=MODEL_MAIN,
    contents="Summarize yesterday's claims by category.",
    config=types.GenerateContentConfig(
        service_tier=types.ServiceTier.FLEX,          # the report is not urgent: cheaper
        labels={"team": "analytics", "feature": "daily-claims-report"},
        http_options=types.HttpOptions(timeout=120_000),  # FLEX may take longer to respond
    ),
)
print(resp.usage_metadata.traffic_type)   # who actually served the request
