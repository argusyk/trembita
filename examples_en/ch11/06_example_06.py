# Chapter 11. Multimodal Understanding and Structured Responses – example 6 (manuscript: 11-multymodalnist.md, line 294)
import enum
from google import genai
from google.genai import types

class DocType(enum.Enum):
    CMR = "CMR"
    TTN = "TTN"
    INVOICE = "invoice"
    OTHER = "other"

client = genai.Client()
resp = client.models.generate_content(
    model="gemini-3.1-flash-lite",                  # a cheap model for sorting
    contents=[types.Part.from_bytes(data=open("doc.jpg", "rb").read(),
                                    mime_type="image/jpeg"),
              "What type of document is this?"],
    config=types.GenerateContentConfig(
        response_mime_type="text/x.enum",
        response_schema=DocType,
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW,
    ),
)
print(resp.parsed)            # DocType.CMR
