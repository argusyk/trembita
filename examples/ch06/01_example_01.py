# Розділ 6. Родина моделей Gemini і відкриті моделі Gemma – приклад 1 (рукопис: 06-rodyna-modeley.md, рядок 72)
from google import genai
from google.genai import types

from trembita.config import MODEL_MAIN

client = genai.Client()

# Нічний звіт для аналітиків: терміни гнучкі, ціна важливіша за швидкість
resp = client.models.generate_content(
    model=MODEL_MAIN,
    contents="Підсумуй затримки рейсів за тиждень за цими записами: ...",
    config=types.GenerateContentConfig(service_tier=types.ServiceTier.FLEX),
)
usage = resp.usage_metadata
if usage is not None:
    # ON_DEMAND, ON_DEMAND_FLEX, ON_DEMAND_PRIORITY, PROVISIONED_THROUGHPUT ...
    print(usage.traffic_type, usage.total_token_count)
