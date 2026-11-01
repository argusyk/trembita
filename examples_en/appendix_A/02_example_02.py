# Appendix A. Laboratory Practicum – example 2 (manuscript: 90-appendix-a.md, line 138)
import enum
from google import genai
from google.genai import types

class Intent(enum.Enum):
    AVAILABILITY = "availability"
    PRICE = "price"
    BOOKING = "booking"
    COMPLAINT = "complaint"
    OTHER = "other"

TESTS = [("Do you have ibuprofen at the pharmacy in Sykhiv?", Intent.AVAILABILITY), ...]  # 30 rows

def accuracy(instruction: str, model: str = "gemini-3.1-flash-lite") -> float:
    client = genai.Client()
    cfg = types.GenerateContentConfig(system_instruction=instruction,   # temperature – default
                                      response_mime_type="text/x.enum", response_schema=Intent)
    hits = sum(client.models.generate_content(model=model, contents=text, config=cfg).parsed == gold
               for text, gold in TESTS)
    return hits / len(TESTS)
