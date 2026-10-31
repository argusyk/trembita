# Додаток Г. Довідник рецептів коду – приклад 21 (рукопис: 93-dodatok-g.md, рядок 400)
import enum

class DocType(enum.Enum):
    CMR = "CMR"
    TTN = "ТТН"
    OTHER = "інше"

resp = client.models.generate_content(
    model="gemini-3.1-flash-lite",
    contents=[types.Part.from_bytes(data=photo, mime_type="image/jpeg"), "Тип документа?"],
    config=types.GenerateContentConfig(response_mime_type="text/x.enum", response_schema=DocType),
)
print(resp.parsed)                           # DocType.CMR
