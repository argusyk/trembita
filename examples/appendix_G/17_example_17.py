# Додаток Г. Довідник рецептів коду – приклад 17 (рукопис: 93-dodatok-g.md, рядок 314)
photo = open("cmr_SM-2610-0042.jpg", "rb").read()
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[
        types.Part.from_bytes(data=photo, mime_type="image/jpeg",
            media_resolution=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_HIGH),
        "Що це за документ? Перелічи заповнені графи й познач нерозбірливі.",
    ],
)
print(resp.text, resp.usage_metadata.prompt_token_count)
