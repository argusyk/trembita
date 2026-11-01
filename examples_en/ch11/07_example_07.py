# Chapter 11. Multimodal Understanding and Structured Responses – example 7 (manuscript: 11-multymodalnist.md, line 342)
from pydantic import BaseModel, Field
from google import genai
from google.genai import types

class Detection(BaseModel):
    label: str = Field(description="What was found: 'damaged pallet', 'torn film'...")
    box_2d: list[int] = Field(description="[ymin, xmin, ymax, xmax], normalized to 0–1000")

def to_pixels(det: Detection, width: int, height: int) -> tuple[int, int, int, int]:
    """Returns (x1, y1, x2, y2) in pixels – the PIL and OpenCV format."""
    ymin, xmin, ymax, xmax = det.box_2d
    return (round(xmin / 1000 * width), round(ymin / 1000 * height),
            round(xmax / 1000 * width), round(ymax / 1000 * height))

client = genai.Client()
frame = types.Part.from_bytes(data=open("cam3_06-07-41.jpg", "rb").read(),
                              mime_type="image/jpeg")
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[frame, "Find damaged pallets, boxes and torn film. "
                     "For each object return a label and box_2d."],
    config=types.GenerateContentConfig(response_mime_type="application/json",
                                       response_schema=list[Detection]),
)
for det in resp.parsed or []:             # None if parsing failed
    print(det.label, to_pixels(det, 1920, 1080))
