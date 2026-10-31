# Додаток Г. Довідник рецептів коду – приклад 18 (рукопис: 93-dodatok-g.md, рядок 330)
contract = client.files.upload(file="dohovir_perevezennia_2026.pdf")
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[contract, "Знайди пункти про відповідальність перевізника, "
                        "вкажи сторінку й процитуй головне речення."],
    config=types.GenerateContentConfig(
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_MEDIUM),
)
print(resp.text)
