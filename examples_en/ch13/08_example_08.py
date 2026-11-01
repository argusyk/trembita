# Chapter 13. Optimization: context caching, batch processing and cost – example 8 (manuscript: 13-optymizatsiya.md, line 374)
import enum
from google import genai
from google.genai import types
from trembita.config import MODEL_LITE, MODEL_MAIN, MODEL_SMART

client = genai.Client()


class Route(enum.Enum):
    SIMPLE = "simple"        # reference: status, warehouse schedule
    STANDARD = "standard"    # calculation, explanation of rules
    COMPLEX = "complex"      # claim, dispute, customs, legal nuances


ROUTER = ("Assess the complexity of a request to the logistics company Smereka "
          "and return one class: simple, standard or complex.\nRequest: ")
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
        return Route.STANDARD                 # in doubt: the middle route, not the cheapest one


def answer(question: str) -> str:
    model, level = PLAN[classify(question)]
    resp = client.models.generate_content(
        model=model, contents=question,
        config=types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_level=level)),
    )
    return resp.text
