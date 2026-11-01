# Chapter 6. The Gemini Model Family and the Open Gemma Models – example 1 (manuscript: 06-rodyna-modeley.md, line 72)
from google import genai
from google.genai import types

from trembita.config import MODEL_MAIN

client = genai.Client()

# Nightly report for the analysts: timing is flexible, price matters more than speed
resp = client.models.generate_content(
    model=MODEL_MAIN,
    contents="Summarize this week's trip delays based on these records: ...",
    config=types.GenerateContentConfig(service_tier=types.ServiceTier.FLEX),
)
usage = resp.usage_metadata
if usage is not None:
    # ON_DEMAND, ON_DEMAND_FLEX, ON_DEMAND_PRIORITY, PROVISIONED_THROUGHPUT ...
    print(usage.traffic_type, usage.total_token_count)
