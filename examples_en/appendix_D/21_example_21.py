# Appendix D. Code Recipes – example 21 (manuscript: 93-appendix-d.md, line 404)
import enum

class DocType(enum.Enum):
    CMR = "CMR"
    TTN = "TTN"
    OTHER = "other"

resp = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=[types.Part.from_bytes(data=photo, mime_type="image/jpeg"), "Document type?"],
    config=types.GenerateContentConfig(response_mime_type="text/x.enum", response_schema=DocType),
)
print(resp.parsed)                           # DocType.CMR
