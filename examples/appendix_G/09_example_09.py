# Додаток Г. Довідник рецептів коду – приклад 9 (рукопис: 93-dodatok-g.md, рядок 150)
resp = client.models.generate_content(
    model="gemini-4-argon",
    contents="70 палет по 420 кг, напівпричіп бере 33 палетомісця й 24 т. Скільки рейсів?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="medium")),
)
um = resp.usage_metadata
print("думки:", um.thoughts_token_count, "відповідь:", um.candidates_token_count)
billed_out = (um.thoughts_token_count or 0) + (um.candidates_token_count or 0)
