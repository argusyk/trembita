"""Надійний клієнт «Трембіти» (розділи 7 і 23).

Промисловий стан (розділ 23): повтори виконує SDK – make_client() налаштовує
types.HttpOptions(retry_options=types.HttpRetryOptions(...), timeout=...). Понад ним стоїть
ask_with_fallback(): автоматичні вимикачі й ланцюг резервних моделей у межах бюджету часу; там
повтори SDK вимкнено (attempts=1), щоб повторював рівно один рівень.

backoff_delays() і with_retries() – НАВЧАЛЬНА версія розділу 7 (повний джитер, Retry-After).
Пакет нею сам не користується; вона годиться для викликів поза SDK і для експериментів.
Не загортайте в неї виклики клієнта з make_client(): повтори множитимуться.
"""
import random
import time

import httpx
from google import genai
from google.genai import errors, types

from .config import MODEL_FALLBACK, MODEL_LITE, MODEL_MAIN
from .prompts import SYSTEM_INSTRUCTION

RETRYABLE = (408, 429, 500, 502, 503, 504)          # ті самі коди, що повторює SDK
TRANSIENT_NETWORK = (httpx.TimeoutException, httpx.ConnectError)   # SDK повторює й кидає саме їх


# ---------- клієнт (розділ 23) ----------
def retry_options(attempts: int = 3, initial_delay: float = 1.0, max_delay: float = 8.0) -> types.HttpRetryOptions:
    """Політика повторів SDK: attempts – разом із першою спробою; attempts=1 – без повторів."""
    return types.HttpRetryOptions(attempts=attempts, initial_delay=initial_delay, max_delay=max_delay,
                                  exp_base=2.0, jitter=1.0, http_status_codes=list(RETRYABLE))


def make_client(*, attempts: int = 3, timeout_ms: int = 20_000, max_delay: float = 8.0,
                **kwargs) -> genai.Client:
    """Клієнт Gemini з тайм-аутом (МІЛІСЕКУНДИ) і повторами в SDK.

    Developer API – ключ із GEMINI_API_KEY. Agent Platform – vertexai=True, project=..., location=...
    або змінні GOOGLE_GENAI_USE_VERTEXAI, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION.
    Власний http_options у kwargs замінює типові налаштування повністю.
    """
    kwargs.setdefault("http_options", types.HttpOptions(
        timeout=timeout_ms, retry_options=retry_options(attempts, max_delay=max_delay)))
    return genai.Client(**kwargs)


def ask(question: str, *, model: str = MODEL_MAIN, client=None, thinking_level: str = "low") -> str:
    """Одне запитання – одна відповідь із системною інструкцією «Трембіти» (повтори – у SDK)."""
    client = client or make_client()
    config = types.GenerateContentConfig(
        system_instruction=SYSTEM_INSTRUCTION,
        thinking_config=types.ThinkingConfig(thinking_level=thinking_level),
    )
    resp = client.models.generate_content(model=model, contents=question, config=config)
    return resp.text or ""


# ---------- вимикач і резервні моделі (розділ 23.4) ----------
class CircuitBreaker:
    """Після threshold невдач поспіль «розмикається» на cooldown секунд (у багатопотоковому сервісі – з блокуванням)."""

    def __init__(self, threshold: int = 5, cooldown: float = 30.0, clock=time.monotonic):
        self.threshold, self.cooldown, self.clock = threshold, cooldown, clock
        self.failures, self.opened_at = 0, None

    def allow(self) -> bool:
        if self.opened_at is None:
            return True                                              # замкнено
        return self.clock() - self.opened_at >= self.cooldown         # напіввідкрито: пробний запит

    def record(self, ok: bool) -> None:
        if ok:
            self.failures, self.opened_at = 0, None                  # знову замкнено
        else:
            self.failures += 1
            if self.failures >= self.threshold:
                self.opened_at = self.clock()                        # розімкнено на паузу


FALLBACK_CHAIN = (MODEL_MAIN, MODEL_FALLBACK, MODEL_LITE)
BREAKERS: dict[str, CircuitBreaker] = {}
FALLBACK_ANSWER = "Зараз «Трембіта» перевантажена. Диспетчер відповість вам особисто."


def _is_transient(e: Exception) -> bool:
    """Тимчасова помилка, після якої варто йти до резервної моделі."""
    if isinstance(e, errors.APIError):
        return e.code in RETRYABLE
    return isinstance(e, TRANSIENT_NETWORK)


def ask_with_fallback(client, question: str, *, chain=FALLBACK_CHAIN, breakers=None,
                      deadline_s: float = 10.0, min_call_s: float = 1.0,
                      config: types.GenerateContentConfig | None = None, clock=time.monotonic) -> str:
    """Відповідь першої доступної моделі ланцюга в межах бюджету часу deadline_s.

    Кожна модель отримує одну спробу з тайм-аутом = залишок бюджету (повтори SDK вимкнено).
    429, 5xx, 408 і мережеві тайм-аути/з'єднання – перехід до наступної моделі; 400/403/404 – виняток
    нагору: це помилка в запиті, правах чи назві моделі, і резерв лише замаскував би її.
    """
    breakers = BREAKERS if breakers is None else breakers
    start = clock()
    for model in chain:
        breaker = breakers.setdefault(model, CircuitBreaker(clock=clock))
        if not breaker.allow():
            continue
        remaining = deadline_s - (clock() - start)
        if remaining < min_call_s:
            break                                   # на ще один виклик часу немає
        base = config.model_copy() if config else types.GenerateContentConfig()
        base.http_options = types.HttpOptions(timeout=int(remaining * 1000),
                                              retry_options=retry_options(attempts=1))
        try:
            resp = client.models.generate_content(model=model, contents=question, config=base)
        except (errors.APIError, *TRANSIENT_NETWORK) as e:
            if not _is_transient(e):
                raise
            breaker.record(False)
            continue
        breaker.record(True)
        return resp.text or ""
    return FALLBACK_ANSWER


# ---------- НАВЧАЛЬНА версія повторів (розділ 7) ----------
def backoff_delays(attempts: int, base: float = 1.0, cap: float = 30.0, rng=random.random) -> list[float]:
    """Затримки «повний джитер» (7.4): випадкове значення з [0, min(cap, base·2^k)]."""
    return [rng() * min(cap, base * 2 ** k) for k in range(attempts - 1)]


def retry_after_seconds(e: Exception) -> float | None:
    """Пауза із заголовка Retry-After (у секундах), якщо сервер її надіслав."""
    headers = getattr(getattr(e, "response", None), "headers", None) or {}
    value = headers.get("retry-after") or headers.get("Retry-After")
    try:
        return max(0.0, float(value)) if value is not None else None
    except (TypeError, ValueError):
        return None                                  # формат HTTP-дати не розбираємо


def with_retries(call, attempts: int = 5, sleep=time.sleep, delays=None, cap: float = 30.0):
    """Викликає call(), повторюючи на 408/429/5xx і мережевих збоях; інші помилки – одразу нагору.

    Пауза – повний джитер, але не менша за Retry-After (і не більша за cap).
    """
    delays = delays if delays is not None else backoff_delays(attempts, cap=cap)
    for k in range(attempts):
        try:
            return call()
        except (errors.APIError, *TRANSIENT_NETWORK) as e:
            if not _is_transient(e) or k == attempts - 1:
                raise                                # 400, 403, 404 – одразу нагору
            sleep(min(cap, max(delays[k], retry_after_seconds(e) or 0.0)))
