"""Оцінювання «Трембіти» (розділ 20): метрики, статистика, суддя й класифікатор намірів."""
import math
import re
from collections import Counter
from enum import Enum
from typing import Literal

from google.genai import types
from pydantic import BaseModel, Field

from .client import make_client
from .config import MODEL_LITE, MODEL_SMART


# ---------- точні метрики ----------
def tokens(s: str) -> list[str]:
    return re.findall(r"[\w'-]+", s.lower())        # \w у Python 3 розуміє кирилицю


def exact_match(pred: str, gold: str) -> bool:
    return tokens(pred) == tokens(gold)


def token_f1(pred: str, gold: str) -> float:
    p, g = tokens(pred), tokens(gold)
    common = sum((Counter(p) & Counter(g)).values())
    if not common:
        return 0.0
    prec, rec = common / len(p), common / len(g)
    return 2 * prec * rec / (prec + rec)


def per_class(preds: list[str], golds: list[str]) -> dict[str, tuple[float, float, float]]:
    """Влучність, повнота й F1 для кожного класу."""
    out = {}
    for c in sorted(set(golds) | set(preds)):
        tp = sum(p == c and g == c for p, g in zip(preds, golds))
        fp = sum(p == c and g != c for p, g in zip(preds, golds))
        fn = sum(p != c and g == c for p, g in zip(preds, golds))
        pr = tp / (tp + fp) if tp + fp else 0.0
        rc = tp / (tp + fn) if tp + fn else 0.0
        out[c] = (pr, rc, 2 * pr * rc / (pr + rc) if pr + rc else 0.0)
    return out


# ---------- статистика ----------
def mcnemar_p(b: int, c: int) -> float:
    """Двобічне p-значення тесту Мак-Немара; b, c – розбіжності на користь A і B."""
    n = b + c
    if n == 0:
        return 1.0
    if n < 25:                                    # мало розбіжностей: точний біноміальний тест
        k = min(b, c)
        return min(1.0, 2 * sum(math.comb(n, i) for i in range(k + 1)) / 2 ** n)
    chi2 = (abs(b - c) - 1) ** 2 / n
    return math.erfc(math.sqrt(chi2 / 2))         # хвіст хі-квадрат з 1 ступенем свободи


def wilson(k: int, n: int, z: float = 1.96) -> tuple[float, float]:
    """Довірчий інтервал Вілсона для частки k/n."""
    if n == 0:
        return 0.0, 1.0
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return max(0.0, centre - half), min(1.0, centre + half)


def sample_size(p: float, margin: float, z: float = 1.96) -> int:
    """Кількість випадків для оцінки точності p з похибкою margin."""
    return math.ceil(z * z * p * (1 - p) / margin ** 2)


# ---------- моделі в оцінюванні ----------
class Intent(str, Enum):
    tracking = "tracking"
    tariff = "tariff"
    warehouse = "warehouse"
    pickup = "pickup"
    claim = "claim"
    other = "other"


def classify_intent(text: str, client=None) -> str:
    """Намір звернення: дешева модель зі структурованою відповіддю-енумом."""
    resp = (client or make_client()).models.generate_content(
        model=MODEL_LITE, contents=text,
        config=types.GenerateContentConfig(
            system_instruction="Визнач намір звернення до логістичної компанії.",
            response_mime_type="text/x.enum", response_schema=Intent),
    )
    return resp.parsed.value if resp.parsed is not None else Intent.other.value


RUBRIC = """\
Ти – суворий оцінювач відповідей асистента логістичної компанії «Смерека».
Критерії (так/ні):
- correct: відповідь збігається з еталоном за суттю;
- grounded: усі факти підтверджено даними інструментів чи документів;
- actionable: клієнт знає, що робити далі;
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


def judge(question: str, reference: str, answer: str, client=None) -> Verdict:
    resp = (client or make_client()).models.generate_content(
        model=MODEL_SMART,
        contents=(f"<question>{question}</question>\n<reference>{reference}</reference>\n"
                  f"<answer>{answer}</answer>"),
        config=types.GenerateContentConfig(
            system_instruction=RUBRIC, response_mime_type="application/json",
            response_schema=Verdict, thinking_config=types.ThinkingConfig(thinking_level="low")),
    )
    return resp.parsed


class Preference(BaseModel):
    reasoning: str
    winner: Literal["A", "B", "tie"]


def _compare(client, question: str, reference: str, a: str, b: str) -> str:
    resp = client.models.generate_content(
        model=MODEL_SMART,
        contents=(f"<question>{question}</question>\n<reference>{reference}</reference>\n"
                  f"<answer_a>{a}</answer_a>\n<answer_b>{b}</answer_b>"),
        config=types.GenerateContentConfig(
            system_instruction="Порівняй дві відповіді за точністю, повнотою дій і тоном. "
                               "Не віддавай переваги довшій відповіді лише через довжину.",
            response_mime_type="application/json", response_schema=Preference),
    )
    return resp.parsed.winner


def pairwise(question: str, reference: str, x: str, y: str, client=None) -> str:
    """Повертає 'x', 'y' або 'tie'; суперечливі після перестановки вердикти дають нічию."""
    client = client or make_client()
    first = {"A": "x", "B": "y", "tie": "tie"}[_compare(client, question, reference, x, y)]
    second = {"A": "y", "B": "x", "tie": "tie"}[_compare(client, question, reference, y, x)]
    return first if first == second else "tie"
