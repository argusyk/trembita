# Appendix A. Laboratory Practicum – example 5 (manuscript: 90-appendix-a.md, line 265)
from pathlib import Path
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class WorkOrder(BaseModel):                       # variant 3; other variants – your own schema
    number: str = Field(description="Work order number")
    date: str = Field(description="Date in YYYY-MM-DD format")
    car_plate: str = Field(description="Vehicle registration number")
    total_uah: float = Field(description="Amount due, UAH")

client = genai.Client()
scan = Path("naryad_01.jpg").read_bytes()
for level in ("MEDIA_RESOLUTION_LOW", "MEDIA_RESOLUTION_MEDIUM", "MEDIA_RESOLUTION_HIGH"):
    image = types.Part.from_bytes(data=scan, mime_type="image/jpeg", media_resolution=level)
    resp = client.models.generate_content(
        model="gemini-3.8-flash",
        contents=[image, "Fill in the schema from the document. Do not guess what is illegible; leave it empty."],
        config=types.GenerateContentConfig(response_mime_type="application/json",
                                           response_schema=WorkOrder))
    print(level, resp.usage_metadata.prompt_token_count, resp.parsed)
