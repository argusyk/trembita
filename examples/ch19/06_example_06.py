# Розділ 19. Безпека застосунків і ризики – приклад 6 (рукопис: 19-bezpeka-zastosunkiv.md, рядок 253)
from pydantic import BaseModel
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_MAIN

class Claim(BaseModel):
    statement: str
    quote: str                    # дослівний фрагмент регламенту

class GroundedAnswer(BaseModel):
    answer: str
    claims: list[Claim]
    enough_evidence: bool

def _norm(s: str) -> str:
    return " ".join(s.lower().split())

def answer_from_policy(question: str, policy: str) -> str:
    resp = make_client().models.generate_content(
        model=MODEL_MAIN,
        contents=f"Регламент:\n{policy}\n\nПитання клієнта: {question}",
        config=types.GenerateContentConfig(
            system_instruction="Відповідай лише на підставі регламенту. Кожне твердження "
                               "підкріпи дослівною цитатою. Якщо опори немає, постав "
                               "enough_evidence=false і не вигадуй.",
            response_mime_type="application/json",
            response_schema=GroundedAnswer,
        ),
    )
    ga: GroundedAnswer = resp.parsed
    fake = [c for c in ga.claims if _norm(c.quote) not in _norm(policy)]
    if not ga.enough_evidence or not ga.claims or fake:
        return "У регламенті немає прямої відповіді. Передаю питання юристу відділу претензій."
    return ga.answer
