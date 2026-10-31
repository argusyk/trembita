# Додаток А. Практикум – приклад 5 (рукопис: 90-dodatok-a.md, рядок 245)
from pathlib import Path
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class WorkOrder(BaseModel):                       # варіант 3; інші варіанти – власна схема
    number: str = Field(description="Номер наряду-замовлення")
    date: str = Field(description="Дата у форматі РРРР-ММ-ДД")
    car_plate: str = Field(description="Державний номер автомобіля")
    total_uah: float = Field(description="Сума до сплати, грн")

client = genai.Client()
scan = Path("naryad_01.jpg").read_bytes()
for level in ("MEDIA_RESOLUTION_LOW", "MEDIA_RESOLUTION_MEDIUM", "MEDIA_RESOLUTION_HIGH"):
    image = types.Part.from_bytes(data=scan, mime_type="image/jpeg", media_resolution=level)
    resp = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[image, "Заповни схему за документом. Нерозбірливе не вгадуй, залиш порожнім."],
        config=types.GenerateContentConfig(response_mime_type="application/json",
                                           response_schema=WorkOrder))
    print(level, resp.usage_metadata.prompt_token_count, resp.parsed)
