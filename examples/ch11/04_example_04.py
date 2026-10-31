# Розділ 11. Мультимодальне розуміння і структуровані відповіді – приклад 4 (рукопис: 11-multymodalnist.md, рядок 188)
from google import genai

client = genai.Client()

call = client.files.upload(file="dzvinok_vodiy_2610_2347.mp3")
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[
        call,
        "Транскрибуй розмову українською з мітками часу [ХХ:СС] і позначками "
        "«Диспетчер» / «Водій». Потім окремим списком випиши: номер відправлення, "
        "місце, проблему, про що домовилися. Нерозбірливі місця познач [нерозбірливо].",
    ],
)
print(resp.text)
