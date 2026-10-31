# Додаток Г. Довідник рецептів коду – приклад 6 (рукопис: 93-dodatok-g.md, рядок 90)
usage = None
for chunk in client.models.generate_content_stream(
    model="gemini-3.8-flash",
    contents="Поясни водієві, як оформити ТТН на збірний вантаж.",
):
    if chunk.text:                           # службовий фрагмент може не мати тексту
        print(chunk.text, end="", flush=True)
    usage = chunk.usage_metadata or usage    # облік – в останніх фрагментах
print("\nвихідних токенів:", usage.candidates_token_count if usage else "?")
