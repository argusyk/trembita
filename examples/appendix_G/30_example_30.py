# Додаток Г. Довідник рецептів коду – приклад 30 (рукопис: 93-dodatok-g.md, рядок 581)
for level in ["MEDIA_RESOLUTION_LOW", "MEDIA_RESOLUTION_HIGH"]:
    image = types.Part.from_bytes(data=photo, mime_type="image/jpeg", media_resolution=level)
    n = client.models.count_tokens(model="gemini-3.8-flash", contents=[image, "Номер накладної?"])
    print(level, n.total_tokens)

SYSTEM = "Ти – «Трембіта», асистент компанії «Смерека»."
print(client.models.count_tokens(model="gemini-3.8-flash", contents=SYSTEM).total_tokens)
# config=types.CountTokensConfig(system_instruction=SYSTEM) поза Agent Platform – ValueError
