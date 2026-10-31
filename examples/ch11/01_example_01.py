# Розділ 11. Мультимодальне розуміння і структуровані відповіді – приклад 1 (рукопис: 11-multymodalnist.md, рядок 42)
from google import genai
from google.genai import types

client = genai.Client()

with open("cmr_SM-2610-0042.jpg", "rb") as f:
    photo = f.read()

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[
        types.Part.from_bytes(
            data=photo,
            mime_type="image/jpeg",
            # дрібний рукописний текст: просимо більше токенів саме для цього фото
            media_resolution=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_HIGH,
        ),
        "Що це за документ? Перелічи заповнені графи і познач нерозбірливі.",
    ],
)
print(resp.text)
print(resp.usage_metadata.prompt_token_count)   # скільки коштував вхід
