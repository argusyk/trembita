# Chapter 18. Gemini for Knowledge Work: Workspace, NotebookLM, Deep Research and Gemini Enterprise – example 3 (manuscript: 18-znannieva-robota.md, line 274)
# Normalising carriers' price lists into a single table for Sheets
import csv
import pathlib

from pydantic import BaseModel, Field
from google import genai
from google.genai import types
from trembita.config import MODEL_MAIN

client = genai.Client()


class TariffRow(BaseModel):
    carrier: str = Field(description="Carrier name")
    origin: str = Field(description="City of departure")
    destination: str = Field(description="Destination city or country")
    weight_from_kg: float | None = Field(None, description="Lower weight limit, if given")
    weight_to_kg: float | None = Field(None, description="Upper weight limit, if given")
    price: float | None = Field(None, description="Rate excluding VAT, as in the document")
    currency: str | None = Field(None, description="Currency of the rate, as in the document: EUR, PLN, UAH")
    unit: str | None = Field(None, description="What the rate is for: kg, pallet, trip, 100 kg")
    fuel_surcharge_pct: float | None = Field(None, description="Fuel surcharge, %")
    source_page: int = Field(description="PDF page where the rate was found")


rows: list[TariffRow] = []
for pdf in sorted(pathlib.Path("pricelists").glob("*.pdf")):
    resp = client.models.generate_content(
        model=MODEL_MAIN,
        contents=[types.Part.from_bytes(data=pdf.read_bytes(), mime_type="application/pdf"),
                  "Extract all tariff rates. Do not calculate anything; leave missing fields empty."],
        config=types.GenerateContentConfig(response_mime_type="application/json",
                                           response_schema=list[TariffRow]),
    )
    rows.extend(resp.parsed or [])

with open("tariffs.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=list(TariffRow.model_fields))
    writer.writeheader()
    writer.writerows(r.model_dump() for r in rows)
