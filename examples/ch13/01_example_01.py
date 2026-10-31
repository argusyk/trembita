# Розділ 13. Оптимізація: кешування контексту, пакетна обробка й вартість – приклад 1 (рукопис: 13-optymizatsiya.md, рядок 52)
from google.genai import types

# Ціни за 1 млн токенів, дол. Орієнтир на момент написання (жовтень 2026 року);
# тримайте їх у конфігурації, а не в коді: з 01.01.2027 ціна кешу зміниться.
PRICES = {
    "gemini-3.8-flash": {"in": 0.75, "cached": 0.0375, "out": 3.75},
    # інші моделі додайте зі сторінки цін, не вгадуючи ціну кешу
}


def request_cost(usage: types.GenerateContentResponseUsageMetadata,
                 model: str = "gemini-3.8-flash") -> float:
    """Вартість одного запиту за формулою (13.1), без зберігання кешу й тарифу інструментів."""
    p = PRICES[model]
    prompt = usage.prompt_token_count or 0
    cached = usage.cached_content_token_count or 0
    tool_in = usage.tool_use_prompt_token_count or 0
    out = (usage.candidates_token_count or 0) + (usage.thoughts_token_count or 0)
    fresh = prompt - cached + tool_in          # вхід за повною ціною
    return (fresh * p["in"] + cached * p["cached"] + out * p["out"]) / 1_000_000
