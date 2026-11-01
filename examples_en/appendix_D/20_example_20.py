# Appendix D. Code Recipes – example 20 (manuscript: 93-appendix-d.md, line 373)
from pydantic import BaseModel, Field

class CargoItem(BaseModel):
    name: str
    packages: int
    weight_kg: float = Field(description="Gross weight, kg (CMR box 11)")

class Waybill(BaseModel):
    number: str
    date: str = Field(description="Date in YYYY-MM-DD format")
    items: list[CargoItem]

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[types.Part.from_bytes(data=photo, mime_type="image/jpeg"),
              "Extract the data from the CMR waybill."],
    config=types.GenerateContentConfig(response_mime_type="application/json",
                                       response_schema=Waybill),   # or list[Waybill]
)
waybill = resp.parsed                        # None if the response did not pass the schema
if waybill is None:
    print("Manual processing needed:", (resp.text or "")[:200])
else:
    print(waybill.number, sum(i.weight_kg for i in waybill.items))
