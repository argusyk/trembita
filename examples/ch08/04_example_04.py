# Розділ 8. Інженерія підказок для Gemini – приклад 4 (рукопис: 08-pidkazky.md, рядок 212)
from google import genai
from google.genai import types

client = genai.Client()


def image(path: str) -> types.Part:
    return types.Part.from_bytes(data=open(path, "rb").read(), mime_type="image/jpeg")


contents = [
    "Фото 1 – накладна CMR:", image("cmr_SM-2610-0388.jpg"),
    "Фото 2 – пломба на дверях причепа:", image("seal_SM-2610-0388.jpg"),
    """Завдання:
1. Випиши номер пломби з Фото 1 (графа з відмітками перевізника) і з Фото 2.
2. Порівняй їх символ за символом.
Якщо номер на будь-якому фото нечитабельний, напиши «не видно», не вгадуй.
Формат: «CMR: ... | Пломба: ... | Збіг: так/ні/невідомо».""",
]
resp = client.models.generate_content(model="gemini-3.8-flash", contents=contents)
print(resp.text)
