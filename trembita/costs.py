"""Розрахунок вартості й кешування (розділи 3 і 13)."""
from .config import BATCH_DISCOUNT, PRICES

M = 1_000_000


def request_cost(model: str, prompt_tokens: int, output_tokens: int, cached_tokens: int = 0,
                 thoughts_tokens: int = 0, batch: bool = False) -> float:
    """Вартість одного запиту, дол. Токени мислення тарифікуються як вихідні."""
    p_in, p_out, p_cache = PRICES[model]
    fresh = max(0, prompt_tokens - cached_tokens)
    cost = (fresh * p_in + cached_tokens * p_cache + (output_tokens + thoughts_tokens) * p_out) / M
    return cost * (BATCH_DISCOUNT if batch else 1.0)


def cost_from_usage(model: str, usage) -> float:
    """Вартість за usage_metadata відповіді generate_content."""
    return request_cost(model, usage.prompt_token_count or 0, usage.candidates_token_count or 0,
                        usage.cached_content_token_count or 0, usage.thoughts_token_count or 0)


def cache_break_even(prefix_tokens: int, model: str, storage_per_hour: float, hours: float) -> float:
    """Скільки запитів за час зберігання кешу треба зробити, щоб кеш окупився.

    Економія на запиті: T·(p_in − p_cache); витрати: T·s·h. Окупність: n > s·h / (p_in − p_cache).
    """
    p_in, _, p_cache = PRICES[model]
    return storage_per_hour * hours / (p_in - p_cache)
