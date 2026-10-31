# Розділ 20. Оцінювання застосунків на Gemini – приклад 2 (рукопис: 20-otsiniuvannia.md, рядок 149)
from pydantic import BaseModel, Field
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_SMART

RUBRIC = """Ти оцінюєш відповідь асистента логістичної компанії «Смерека».
Критерії (так/ні):
- correct: номери, дати, суми й факти не суперечать еталону;
- grounded: немає тверджень, яких нема ні в еталоні, ні в даних інструментів;
- actionable: клієнт розуміє, що робити далі;
- tone: ввічливо, українською, без канцеляриту.
Спершу коротко обґрунтуй, потім заповни критерії й постав загальний бал 1-5.
Довжина відповіді сама по собі не є ні перевагою, ні недоліком."""

class Verdict(BaseModel):
    reasoning: str = Field(description="2-4 речення обґрунтування")
    correct: bool
    grounded: bool
    actionable: bool
    tone: bool
    score: int = Field(ge=1, le=5)

def judge(question: str, reference: str, answer: str) -> Verdict:
    resp = make_client().models.generate_content(
        model=MODEL_SMART,
        contents=(f"<question>{question}</question>\n<reference>{reference}</reference>\n"
                  f"<answer>{answer}</answer>"),
        config=types.GenerateContentConfig(
            system_instruction=RUBRIC,
            response_mime_type="application/json",
            response_schema=Verdict,
            thinking_config=types.ThinkingConfig(thinking_level="low"),
        ),
    )
    return resp.parsed
