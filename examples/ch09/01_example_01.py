# Розділ 9. Мислення: рівні, бюджети й підписи думок – приклад 1 (рукопис: 09-myslennia.md, рядок 30)
from google import genai
from google.genai import types

client = genai.Client()

resp = client.models.generate_content(
    model="gemini-4-argon",
    contents="Вантаж 18 палет по 420 кг. Тягач бере 24 т, напівпричіп – 33 палетомісця. "
             "Скільки рейсів потрібно для 70 палет і чи вистачить одного тягача на день?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="medium"),
    ),
)
print(resp.text)
um = resp.usage_metadata
print("думки:", um.thoughts_token_count, "відповідь:", um.candidates_token_count)
