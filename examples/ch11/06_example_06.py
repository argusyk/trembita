# Розділ 11. Мультимодальне розуміння і структуровані відповіді – приклад 6 (рукопис: 11-multymodalnist.md, рядок 294)
import enum
from google import genai
from google.genai import types

class DocType(enum.Enum):
    CMR = "CMR"
    TTN = "ТТН"
    INVOICE = "рахунок-фактура"
    OTHER = "інше"

client = genai.Client()
resp = client.models.generate_content(
    model="gemini-3.1-flash-lite",                  # дешева модель для сортування
    contents=[types.Part.from_bytes(data=open("doc.jpg", "rb").read(),
                                    mime_type="image/jpeg"),
              "Який це тип документа?"],
    config=types.GenerateContentConfig(
        response_mime_type="text/x.enum",
        response_schema=DocType,
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW,
    ),
)
print(resp.parsed)            # DocType.CMR
