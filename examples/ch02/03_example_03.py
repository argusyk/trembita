# Розділ 2. Архітектура: трансформер, суміш експертів і мультимодальність – приклад 3 (рукопис: 02-arkhitektura.md, рядок 406)
from google import genai
from google.genai import types

client = genai.Client()
response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Продовж фразу одним словом: Вантаж SM-2609-0315 прибув до",
    config=types.GenerateContentConfig(
        temperature=1.0,         # для Gemini 3+ рекомендовано лишати 1.0
        top_p=0.95,              # ядерний відбір
        top_k=40,                # обрізання хвоста
        seed=42,                 # відтворюваність, наскільки її підтримує сервіс
        response_logprobs=True,  # повернути логарифми ймовірностей
        logprobs=5,              # п'ять найкращих кандидатів на кожному кроці
    ),
)
lp = response.candidates[0].logprobs_result
if lp and lp.top_candidates:     # не всі моделі повертають logprobs
    for cand in lp.top_candidates[0].candidates:
        print(cand.token, round(cand.log_probability, 3))
