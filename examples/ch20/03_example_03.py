# Розділ 20. Оцінювання застосунків на Gemini – приклад 3 (рукопис: 20-otsiniuvannia.md, рядок 199)
from typing import Literal
from pydantic import BaseModel
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_SMART

class Preference(BaseModel):
    reasoning: str
    winner: Literal["A", "B", "tie"]

def _compare(question: str, reference: str, a: str, b: str) -> str:
    resp = make_client().models.generate_content(
        model=MODEL_SMART,
        contents=(f"<question>{question}</question>\n<reference>{reference}</reference>\n"
                  f"<answer_a>{a}</answer_a>\n<answer_b>{b}</answer_b>"),
        config=types.GenerateContentConfig(
            system_instruction="Порівняй дві відповіді за точністю, повнотою дій і тоном. "
                               "Не віддавай переваги довшій відповіді лише через довжину.",
            response_mime_type="application/json",
            response_schema=Preference,
        ),
    )
    return resp.parsed.winner

def pairwise(question: str, reference: str, x: str, y: str) -> str:
    """Повертає 'x', 'y' або 'tie'; суперечливі вердикти дають нічию."""
    first = {"A": "x", "B": "y", "tie": "tie"}[_compare(question, reference, x, y)]
    second = {"A": "y", "B": "x", "tie": "tie"}[_compare(question, reference, y, x)]
    return first if first == second else "tie"
