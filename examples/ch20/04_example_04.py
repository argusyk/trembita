# Розділ 20. Оцінювання застосунків на Gemini – приклад 4 (рукопис: 20-otsiniuvannia.md, рядок 212)
from typing import Literal
from pydantic import BaseModel
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_MAIN, MODEL_SMART

class Preference(BaseModel):
    reasoning: str
    winner: Literal["A", "B", "tie"]

def _compare(client, question: str, reference: str, a: str, b: str, model: str) -> str:
    resp = client.models.generate_content(
        model=model,
        contents="\n".join([_tag("question", question), _tag("reference", reference),
                            _tag("answer_a", a), _tag("answer_b", b)]),
        config=types.GenerateContentConfig(
            system_instruction=PAIRWISE_INSTRUCTION,     # точність, дії, тон; довжина – не перевага
            response_mime_type="application/json", response_schema=Preference),
    )
    parsed = resp.parsed
    return getattr(parsed, "winner", "tie") if parsed is not None else "tie"

def pairwise(question: str, reference: str, x: str, y: str, *, model: str = MODEL_SMART,
             generator_models=(MODEL_MAIN,), client=None) -> str:
    """Повертає 'x', 'y' або 'tie'; суперечливі після перестановки вердикти дають нічию."""
    _check_judge(model, generator_models)
    client = client or make_client()
    first = {"A": "x", "B": "y", "tie": "tie"}[_compare(client, question, reference, x, y, model)]
    second = {"A": "y", "B": "x", "tie": "tie"}[_compare(client, question, reference, y, x, model)]
    return first if first == second else "tie"
