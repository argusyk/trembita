# Додаток Г. Довідник рецептів коду – приклад 33 (рукопис: 93-dodatok-g.md, рядок 647)
resp = client.models.generate_content(
    model="gemini-3.1-flash-image",
    contents="Схема для водіїв: як закріпити палети ременями. Світлий фон, без написів.",
    config=types.GenerateContentConfig(
        response_modalities=["TEXT", "IMAGE"],
        image_config=types.ImageConfig(aspect_ratio="16:9")),
)
for i, part in enumerate(resp.parts):
    if part.inline_data:
        part.as_image().save(f"kriplennia_{i}.png")
    elif part.text:
        print(part.text)                         # модель може коментувати результат
