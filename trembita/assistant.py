"""Ручний цикл виклику функцій для інтерфейсу диспетчерської (розділ 10).

Модель бачить три функції читання і create_pickup. Виклик create_pickup лише ставить заявку в чергу
PickupGuard; створює її confirm() – або одразу, якщо оператор схвалив її функцією confirm,
або пізніше з черги диспетчерської. Модель сама заявку не створить ніколи.
"""
from google.genai import types

from . import tools
from .config import MODEL_MAIN
from .pickup_guard import PickupGuard, default_guard
from .prompts import SYSTEM_INSTRUCTION

REGISTRY = {f.__name__: f for f in tools.READ_ONLY + [tools.create_pickup]}


def build_config() -> types.GenerateContentConfig:
    """Конфігурація ручного циклу: функції Python лише для оголошень, AFC вимкнено."""
    return types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        tools=list(REGISTRY.values()),
        automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
    )


def run_tool(name: str, args: dict, *, confirm=None, guard: PickupGuard | None = None,
             operator: str = "оператор") -> dict:
    """Виконує інструмент і завжди повертає словник (помилку – як {"error": ...}).

    create_pickup іде через guard.propose(); якщо передано confirm(name, args) -> bool, людина
    вирішує одразу: True – guard.confirm(), False – guard.reject(). Без confirm заявка чекає в черзі.
    """
    if name not in REGISTRY:
        return {"error": f"невідомий інструмент {name}"}
    try:
        if name not in tools.WITH_EFFECTS:
            return REGISTRY[name](**args)
        guard = guard or default_guard()
        proposal = guard.propose(**args)
    except TypeError as e:                       # модель передала зайві чи неправильні аргументи
        return {"error": f"неправильні аргументи: {e}"}
    if proposal["status"] != "awaiting_human_confirmation" or confirm is None:
        return proposal
    if confirm(name, args):
        return guard.confirm(proposal["token"], operator)
    return guard.reject(proposal["token"], operator, "оператор не підтвердив заявку")


def chat_turn(client, history: list, user_text: str, *, model: str = MODEL_MAIN, confirm=None,
              guard: PickupGuard | None = None, max_steps: int = 6) -> str:
    """Один хід розмови: модель може кілька разів викликати інструменти, доки не дасть текст."""
    history.append(types.Content(role="user", parts=[types.Part(text=user_text)]))
    config = build_config()
    for _ in range(max_steps):
        resp = client.models.generate_content(model=model, contents=history, config=config)
        if not resp.candidates or resp.candidates[0].content is None:
            feedback = getattr(resp, "prompt_feedback", None)
            reason = getattr(feedback, "block_reason", None)
            return f"Запит не опрацьовано{f' ({reason})' if reason else ''}. Спробуйте переформулювати."
        history.append(resp.candidates[0].content)   # разом із підписами думок
        calls = resp.function_calls or []
        if not calls:
            return resp.text or ""
        parts = [types.Part(function_response=types.FunctionResponse(
                     id=c.id, name=c.name,
                     response=run_tool(c.name, dict(c.args or {}), confirm=confirm, guard=guard)))
                 for c in calls]
        history.append(types.Content(role="user", parts=parts))
    return "Не вдалося завершити запит за відведену кількість кроків."
