import httpx
import pytest
from google.genai import errors, types

from trembita import client


def api_error(code):
    cls = errors.ServerError if code >= 500 else errors.ClientError
    return cls(code, {"error": {"message": "x", "status": "S"}})


# ---------- make_client ----------
def test_make_client_sets_timeout_and_sdk_retries():
    c = client.make_client(api_key="test-key")
    opts = c._api_client._http_options
    assert opts.timeout == 20_000
    assert opts.retry_options.attempts == 3 and 429 in opts.retry_options.http_status_codes


# ---------- ask_with_fallback ----------
class Clock:
    def __init__(self):
        self.t = 0.0

    def __call__(self):
        return self.t


class FakeModels:
    def __init__(self, behaviour, clock=None, cost=0.0):
        self.behaviour, self.calls, self.clock, self.cost = behaviour, [], clock, cost

    def generate_content(self, model, contents, config):
        self.calls.append((model, config.http_options.timeout, config.http_options.retry_options.attempts))
        if self.clock:
            self.clock.t += self.cost
        outcome = self.behaviour[model]
        if isinstance(outcome, Exception):
            raise outcome
        return type("R", (), {"text": outcome})()


def run(behaviour, **kw):
    models = FakeModels(behaviour, kw.pop("clock_obj", None), kw.pop("cost", 0.0))
    fake = type("C", (), {"models": models})()
    return client.ask_with_fallback(fake, "Де SM-2610-0042?", chain=("main", "fb", "lite"),
                                    breakers={}, **kw), models


@pytest.mark.parametrize("exc", [api_error(503), api_error(429), api_error(500),
                                 httpx.ReadTimeout("t"), httpx.ConnectError("c")])
def test_fallback_on_transient_errors(exc):
    text, models = run({"main": exc, "fb": "резерв", "lite": "?"})
    assert text == "резерв" and [c[0] for c in models.calls] == ["main", "fb"]
    assert all(c[2] == 1 for c in models.calls)           # повтори SDK вимкнено


@pytest.mark.parametrize("code", [400, 403, 404])
def test_client_errors_are_not_masked(code):
    with pytest.raises(errors.ClientError):
        run({"main": api_error(code), "fb": "резерв", "lite": "?"})


def test_deadline_budget_shrinks_timeouts_and_stops():
    clock = Clock()
    text, models = run({"main": httpx.ReadTimeout("t"), "fb": httpx.ReadTimeout("t"), "lite": "ok"},
                       clock_obj=clock, cost=6.0, clock=clock, deadline_s=10.0)
    assert [c[1] for c in models.calls] == [10_000, 4_000]   # друга модель – лише залишок
    assert text == client.FALLBACK_ANSWER                     # на третю часу немає


def test_breaker_opens_and_skips_model():
    clock = Clock()
    breakers = {"main": client.CircuitBreaker(threshold=2, cooldown=30, clock=clock)}
    fake_models = FakeModels({"main": api_error(503), "fb": "резерв", "lite": "?"})
    fake = type("C", (), {"models": fake_models})()
    for _ in range(3):
        client.ask_with_fallback(fake, "q", chain=("main", "fb"), breakers=breakers, clock=clock)
    assert [c[0] for c in fake_models.calls].count("main") == 2   # третій раз main пропущено
    clock.t += 31
    assert breakers["main"].allow()                               # напіввідкрито


# ---------- навчальна версія з розділу 7 ----------
def test_backoff_bounded():
    assert client.backoff_delays(6, base=1, cap=8, rng=lambda: 1.0) == [1, 2, 4, 8, 8]


def test_retries_on_429_and_network_then_succeeds():
    attempts = []

    def call():
        attempts.append(1)
        if len(attempts) == 1:
            raise api_error(429)
        if len(attempts) == 2:
            raise httpx.ConnectError("down")
        return "ok"
    assert client.with_retries(call, sleep=lambda s: None) == "ok" and len(attempts) == 3


def test_no_retry_on_400():
    with pytest.raises(errors.ClientError):
        client.with_retries(lambda: (_ for _ in ()).throw(api_error(400)), sleep=lambda s: None)


def test_retry_after_is_respected():
    resp = httpx.Response(429, headers={"Retry-After": "7"}, request=httpx.Request("POST", "https://x"))
    err = errors.ClientError(429, {"error": {"message": "q"}}, resp)
    assert client.retry_after_seconds(err) == 7.0
    slept, calls = [], []

    def call():
        calls.append(1)
        if len(calls) == 1:
            raise err
        return "ok"
    assert client.with_retries(call, sleep=slept.append, delays=[0.1]) == "ok" and slept == [7.0]


def test_ask_uses_given_client():
    seen = {}

    class M:
        def generate_content(self, model, contents, config):
            seen.update(model=model, cfg=config)
            return type("R", (), {"text": None})()
    assert client.ask("q", client=type("C", (), {"models": M()})()) == ""
    assert isinstance(seen["cfg"], types.GenerateContentConfig) and seen["cfg"].system_instruction
