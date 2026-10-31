# Розділ 23. Промислова експлуатація на Gemini Enterprise Agent Platform – приклад 3 (рукопис: 23-produkshn.md, рядок 150)
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_MAIN

client = make_client()
resp = client.models.generate_content(
    model=MODEL_MAIN,
    contents="Підсумуй учорашні претензії за категоріями.",
    config=types.GenerateContentConfig(
        service_tier=types.ServiceTier.FLEX,          # звіт не терміновий: дешевше
        labels={"team": "analytics", "feature": "daily-claims-report"},
        http_options=types.HttpOptions(timeout=120_000),  # FLEX може відповідати довше
    ),
)
print(resp.usage_metadata.traffic_type)   # хто насправді обслужив запит
