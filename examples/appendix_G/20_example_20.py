# Додаток Г. Довідник рецептів коду – приклад 20 (рукопис: 93-dodatok-g.md, рядок 372)
from pydantic import BaseModel, Field

class CargoItem(BaseModel):
    name: str
    packages: int
    weight_kg: float = Field(description="Вага брутто, кг (графа 11 CMR)")

class Waybill(BaseModel):
    number: str
    date: str = Field(description="Дата у форматі РРРР-ММ-ДД")
    items: list[CargoItem]

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[types.Part.from_bytes(data=photo, mime_type="image/jpeg"),
              "Витягни дані з накладної CMR."],
    config=types.GenerateContentConfig(response_mime_type="application/json",
                                       response_schema=Waybill),   # або list[Waybill]
)
waybill: Waybill = resp.parsed
print(waybill.number, sum(i.weight_kg for i in waybill.items))
