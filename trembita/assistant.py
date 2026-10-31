"""Ручний цикл виклику функцій із підтвердженням дій з наслідками (розділ 10)."""
from google.genai import types

from . import tools
from .config import MODEL_MAIN
from .prompts import SYSTEM_INSTRUCTION

REGISTRY = {f.__name__: f for f in tools.READ_ONLY + [tools.create_pickup]}


def build_config() -> types.GenerateContentConfig:
    return types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=list(REGISTRY.values()),
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )


def run_tool(name: str, args: dict, confirm=lambda name, args: False) -> dict:
    """Виконує інструмент; дії з наслідками – лише якщо confirm(...) повернув True."""
    if name not in REGISTRY:
        return {"error": f"невідомий інструмент {name}"}
    if name in tools.WITH_EFFECTS and not confirm(name, args):
        return {"error": "дію скасовано: немає підтвердження оператора"}
    try:
        return REGISTRY[name](**args)
    except TypeError as e:                       # модель передала зайві чи неправильні аргументи
        return {"error": f"неправильні аргументи: {e}"}


def chat_turn(client, history: list, user_text: str, *, model: str = MODEL_MAIN,
              confirm=lambda name, args: False, max_steps: int = 6) -> str:
    """Один хід розмови: модель може кілька разів викликати інструменти, доки не дасть текст."""
    history.append(types.Content(role="user", parts=[types.Part(text=user_text)]))
    config = build_config()
    for _ in range(max_steps):
        resp = client.models.generate_content(model=model, contents=history, config=config)
        content = resp.candidates[0].content
        history.append(content)                  # разом із підписами думок
        calls = resp.function_calls or []
        if not calls:
            return resp.text or ""
        parts = [types.Part.from_function_response(name=c.name, response=run_tool(c.name, dict(c.args or {}), confirm))
                 for c in calls]
        history.append(types.Content(role="user", parts=parts))
    return "Не вдалося завершити запит за відведену кількість кроків."
