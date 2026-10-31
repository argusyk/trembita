"""Розрахунок вартості запитів і кешування (розділи 3, 9, 13).

Основна функція – cost_from_usage(model, usage): вартість запиту за формулою (13.1) прямо з
resp.usage_metadata. Окремої плати за інструменти (C_інстр) і зберігання кешу вона не враховує.
"""
from .config import BATCH_DISCOUNT, CACHE_STORAGE_PER_HOUR, PRICES, Price

M = 1_000_000


def price_of(model: str) -> Price:
    """Ціни моделі з config.PRICES; невідома модель – KeyError із підказкою."""
    try:
        return PRICES[model]
    except KeyError:
        raise KeyError(f"ціни для {model!r} немає в trembita.config.PRICES – додайте її зі сторінки цін") from None


def request_cost(model: str, prompt_tokens: int, output_tokens: int, cached_tokens: int = 0,
                 thoughts_tokens: int = 0, tool_use_tokens: int = 0, batch: bool = False) -> float:
    """Вартість одного запиту, дол., за формулою (13.1).

    prompt_tokens уже містить кешовану частину (так рахує Gemini); tool_use_tokens – результати
    вбудованих інструментів, тарифікуються як вхід; токени мислення – як вихід.
    """
    p = price_of(model)
    p_cache = p.inp if p.cached is None else p.cached       # невідома ціна кешу – консервативно
    prompt = max(0, prompt_tokens)
    cached = min(max(0, cached_tokens), prompt)
    fresh = prompt - cached + max(0, tool_use_tokens)
    out = max(0, output_tokens) + max(0, thoughts_tokens)
    cost = (fresh * p.inp + cached * p_cache + out * p.out) / M
    return cost * (BATCH_DISCOUNT if batch else 1.0)


def cost_from_usage(model: str, usage, *, batch: bool = False) -> float:
    """Вартість запиту, дол., за resp.usage_metadata (усі поля можуть бути None)."""
    return request_cost(
        model,
        prompt_tokens=usage.prompt_token_count or 0,
        output_tokens=usage.candidates_token_count or 0,
        cached_tokens=usage.cached_content_token_count or 0,
        thoughts_tokens=usage.thoughts_token_count or 0,
        tool_use_tokens=usage.tool_use_prompt_token_count or 0,
        batch=batch,
    )


def usage_summary(model: str, usage, *, batch: bool = False) -> dict:
    """Токени за видами, частка думок і вартість – один запис журналу (розділи 3 і 9)."""
    thoughts = usage.thoughts_token_count or 0
    answer = usage.candidates_token_count or 0
    return {
        "model": model,
        "prompt": usage.prompt_token_count or 0,
        "cached": usage.cached_content_token_count or 0,
        "tool_use": usage.tool_use_prompt_token_count or 0,
        "thoughts": thoughts,
        "answer": answer,
        "thoughts_share": round(thoughts / max(thoughts + answer, 1), 2),
        "cost_usd": round(cost_from_usage(model, usage, batch=batch), 6),
    }


def _storage(model: str, storage_per_hour: float | None) -> float:
    if storage_per_hour is not None:
        return storage_per_hour
    try:
        return CACHE_STORAGE_PER_HOUR[model]
    except KeyError:
        raise KeyError(f"ціни зберігання кешу для {model!r} немає в CACHE_STORAGE_PER_HOUR") from None


def cache_break_even(model: str, hours: float, storage_per_hour: float | None = None) -> float:
    """Поріг окупності явного кешу n* за формулою (13.4): (p_вх + p_зб·T) / (p_вх − p_кеш).

    Враховує створення кешу (запис оплачується як звичайний вхід), зберігання T годин і читання.
    Розмір кешу скорочується: від нього поріг не залежить.
    """
    p = price_of(model)
    if p.cached is None or p.cached >= p.inp:
        return float("inf")                                 # кеш не дає знижки – не окупиться
    return (p.inp + _storage(model, storage_per_hour) * hours) / (p.inp - p.cached)


def cache_costs(model: str, prefix_tokens: int, n_requests: int, hours: float,
                storage_per_hour: float | None = None) -> tuple[float, float]:
    """Вартість префікса за T годин, дол.: без кешу (13.2) і з явним кешем (13.3)."""
    p = price_of(model)
    if p.cached is None:
        raise KeyError(f"ціни кешованих токенів для {model!r} у config.PRICES немає")
    s = prefix_tokens / M
    without = n_requests * s * p.inp
    with_cache = s * p.inp + s * _storage(model, storage_per_hour) * hours + n_requests * s * p.cached
    return without, with_cache
