# Додаток А. Практикум – приклад 2 (рукопис: 90-dodatok-a.md, рядок 118)
import enum
from google import genai
from google.genai import types

class Intent(enum.Enum):
    AVAILABILITY = "наявність"
    PRICE = "ціна"
    BOOKING = "запис"
    COMPLAINT = "скарга"
    OTHER = "інше"

TESTS = [("Чи є ібупрофен в аптеці на Сихові?", Intent.AVAILABILITY), ...]  # 30 рядків

def accuracy(instruction: str, model: str = "gemini-3.1-flash-lite") -> float:
    client = genai.Client()
    cfg = types.GenerateContentConfig(system_instruction=instruction, temperature=0,
                                      response_mime_type="text/x.enum", response_schema=Intent)
    hits = sum(client.models.generate_content(model=model, contents=text, config=cfg).parsed == gold
               for text, gold in TESTS)
    return hits / len(TESTS)
