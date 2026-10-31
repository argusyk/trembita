# Розділ 11. Мультимодальне розуміння і структуровані відповіді – приклад 2 (рукопис: 11-multymodalnist.md, рядок 98)
from google import genai
from google.genai import types

client = genai.Client()

contract = client.files.upload(
    file="dohovir_perevezennia_2026.pdf",
    config=types.UploadFileConfig(display_name="Договір «Смерека» – ТОВ «Карпати Агро»"),
)

question = (
    "Знайди пункти про відповідальність перевізника за пошкодження вантажу. "
    "Для кожного вкажи номер сторінки й пункту та процитуй ключове речення."
)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[contract, question],      # об'єкт File SDK перетворить на file_data
    config=types.GenerateContentConfig(
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_MEDIUM,
    ),
)
print(resp.text)
