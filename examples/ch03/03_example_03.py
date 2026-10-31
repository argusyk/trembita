# Розділ 3. Токени, мультимодальні токени й довгий контекст – приклад 3 (рукопис: 03-tokeny-kontekst.md, рядок 202)
from pathlib import Path
from google import genai
from google.genai import types

client = genai.Client()
scan = Path("cmr_SM-2610-0042.jpg").read_bytes()
levels = ["MEDIA_RESOLUTION_LOW", "MEDIA_RESOLUTION_MEDIUM", "MEDIA_RESOLUTION_HIGH"]

for level in levels:
    # роздільність задаємо для конкретної частини запиту (Gemini 3 і новіші)
    image = types.Part.from_bytes(data=scan, mime_type="image/jpeg",
                                  media_resolution=level)
    resp = client.models.count_tokens(
        model="gemini-3.8-flash",
        contents=[image, "Прочитай номер накладної в графі 4."],
    )
    print(level, resp.total_tokens)
