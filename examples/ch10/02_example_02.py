# Розділ 10. Виклик функцій – приклад 2 (рукопис: 10-funktsii.md, рядок 99)
from google import genai
from google.genai import types
from trembita.config import MODEL_MAIN
from trembita.tools import track_shipment, get_tariff, find_warehouse

REGISTRY = {"track_shipment": track_shipment, "get_tariff": get_tariff,
            "find_warehouse": find_warehouse}

def run_with_tools(client: genai.Client, question: str, tool: types.Tool, max_steps: int = 6) -> str:
    cfg = types.GenerateContentConfig(
        tools=[tool],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )
    history = [types.Content(role="user", parts=[types.Part(text=question)])]
    for _ in range(max_steps):
        resp = client.models.generate_content(model=MODEL_MAIN, contents=history, config=cfg)
        if not resp.function_calls:
            return resp.text                          # модель відповіла текстом
        history.append(resp.candidates[0].content)    # виклики разом із підписами думок
        parts = []
        for fc in resp.function_calls:
            fn = REGISTRY.get(fc.name)
            try:
                result = fn(**(fc.args or {})) if fn else {"error": f"невідома функція {fc.name}"}
            except Exception as exc:                  # помилку повертаємо моделі як дані
                result = {"error": str(exc)}
            parts.append(types.Part(function_response=types.FunctionResponse(
                id=fc.id, name=fc.name, response=result)))
        history.append(types.Content(role="user", parts=parts))
    return "Не вдалося отримати відповідь за відведену кількість кроків."
