# Розділ 13. Оптимізація: кешування контексту, пакетна обробка й вартість – приклад 8 (рукопис: 13-optymizatsiya.md, рядок 374)
import enum
from google import genai
from google.genai import types
from trembita.config import MODEL_LITE, MODEL_MAIN, MODEL_SMART

client = genai.Client()


class Route(enum.Enum):
    SIMPLE = "simple"        # довідка: статус, графік складу
    STANDARD = "standard"    # розрахунок, пояснення правил
    COMPLEX = "complex"      # претензія, спір, митниця, юридичні нюанси


ROUTER = ("Оціни складність звернення до логістичної компанії «Смерека» "
          "і поверни один клас: simple, standard або complex.\nЗвернення: ")
PLAN = {Route.SIMPLE: (MODEL_MAIN, "low"), Route.STANDARD: (MODEL_MAIN, "medium"),
        Route.COMPLEX: (MODEL_SMART, "high")}


def classify(question: str) -> Route:
    resp = client.models.generate_content(
        model=MODEL_LITE, contents=ROUTER + question,
        config=types.GenerateContentConfig(response_mime_type="text/x.enum", response_schema=Route),
    )
    try:
        return Route((resp.text or "").strip())
    except ValueError:
        return Route.STANDARD                 # сумнів – середній маршрут, а не найдешевший


def answer(question: str) -> str:
    model, level = PLAN[classify(question)]
    resp = client.models.generate_content(
        model=model, contents=question,
        config=types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_level=level)),
    )
    return resp.text
