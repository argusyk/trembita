# Додаток Г. Довідник рецептів коду – приклад 10 (рукопис: 93-dodatok-g.md, рядок 166)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Виїзд зі Львова о 18:00, до Ужгорода 270 км, ліміт 70 км/год, "
             "після 4,5 год їзди 45 хв відпочинку. Коли найраніше прибуття?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high", include_thoughts=True)),
)
for part in resp.candidates[0].content.parts:
    if part.text:                            # частина може містити лише підпис
        print("[думки]" if part.thought else "[відповідь]", part.text)
