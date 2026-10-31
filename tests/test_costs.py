import pytest

from trembita import costs


def test_request_cost_counts_thoughts_as_output():
    c = costs.request_cost("gemini-3.8-flash", 1_000_000, 0, thoughts_tokens=1_000_000)
    assert c == pytest.approx(0.75 + 3.75)


def test_cached_tokens_cheaper_and_batch_half():
    full = costs.request_cost("gemini-3.8-flash", 100_000, 1_000)
    cached = costs.request_cost("gemini-3.8-flash", 100_000, 1_000, cached_tokens=90_000)
    assert cached < full
    assert costs.request_cost("gemini-3.8-flash", 100_000, 1_000, batch=True) == pytest.approx(full / 2)


def test_cache_break_even():
    n = costs.cache_break_even(200_000, "gemini-3.8-flash", storage_per_hour=0.5, hours=1)
    assert n == pytest.approx(0.5 / (0.75 - 0.0375))
