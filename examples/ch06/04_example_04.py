# Розділ 6. Родина моделей Gemini і відкриті моделі Gemma – приклад 4 (рукопис: 06-rodyna-modeley.md, рядок 243)
# Та сама Gemma 4 через Gemini API: порівнюємо з 3.8 Flash на одному запиті
question = "Класифікуй лист: 'Палета прийшла з пошкодженим кутом, SM-2610-0117'."
for model in ("gemma-4-31b-it", "gemini-3.8-flash"):
    resp = client.models.generate_content(model=model, contents=question)
    print(model, "|", (resp.text or "").strip()[:120])
