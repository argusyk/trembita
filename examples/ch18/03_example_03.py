# Розділ 18. Gemini для знаннєвої роботи: Workspace, NotebookLM, Deep Research і Gemini Enterprise – приклад 3 (рукопис: 18-znannieva-robota.md, рядок 274)
# Нормалізація прайс-листів перевізників у єдину таблицю для Sheets
import csv
import pathlib

from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from trembita.config import MODEL_MAIN

client = genai.Client()


class TariffRow(BaseModel):
    carrier: str = Field(description="Назва перевізника")
    origin: str = Field(description="Місто відправлення")
    destination: str = Field(description="Місто або країна призначення")
    weight_from_kg: float | None = Field(None, description="Нижня межа ваги, якщо вказана")
    weight_to_kg: float | None = Field(None, description="Верхня межа ваги, якщо вказана")
    price: float | None = Field(None, description="Ставка без ПДВ, як у документі")
    currency: str | None = Field(None, description="Валюта ставки, як у документі: EUR, PLN, UAH")
    unit: str | None = Field(None, description="За що ставка: кг, палета, рейс, 100 кг")
    fuel_surcharge_pct: float | None = Field(None, description="Паливна надбавка, %")
    source_page: int = Field(description="Сторінка PDF, де знайдено ставку")


rows: list[TariffRow] = []
for pdf in sorted(pathlib.Path("pricelists").glob("*.pdf")):
    resp = client.models.generate_content(
        model=MODEL_MAIN,
        contents=[types.Part.from_bytes(data=pdf.read_bytes(), mime_type="application/pdf"),
                  "Витягни всі тарифні ставки. Нічого не обчислюй, відсутні поля лиши порожніми."],
        config=types.GenerateContentConfig(response_mime_type="application/json",
                                           response_schema=list[TariffRow]),
    )
    rows.extend(resp.parsed or [])

with open("tariffs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(TariffRow.model_fields))
    writer.writeheader()
    writer.writerows(r.model_dump() for r in rows)
