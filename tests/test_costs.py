from types import SimpleNamespace as NS

import pytest

from trembita import costs


def usage(**kw):
    fields = ["prompt_token_count", "candidates_token_count", "cached_content_token_count",
              "thoughts_token_count", "tool_use_prompt_token_count"]
    return NS(**{f: kw.get(f) for f in fields})


def test_request_cost_counts_thoughts_as_output():
    c = costs.request_cost("gemini-3.8-flash", 1_000_000, 0, thoughts_tokens=1_000_000)
    assert c == pytest.approx(0.75 + 3.75)


def test_cached_tokens_cheaper_and_batch_half():
    full = costs.request_cost("gemini-3.8-flash", 100_000, 1_000)
    cached = costs.request_cost("gemini-3.8-flash", 100_000, 1_000, cached_tokens=90_000)
    assert cached < full
    assert costs.request_cost("gemini-3.8-flash", 100_000, 1_000, batch=True) == pytest.approx(full / 2)


def test_cost_from_usage_formula_13_1_with_tool_use():
    u = usage(prompt_token_count=1_000_000, cached_content_token_count=400_000,
              tool_use_prompt_token_count=200_000, candidates_token_count=100_000,
              thoughts_token_count=100_000)
    expected = (600_000 + 200_000) * 0.75 / 1e6 + 400_000 * 0.0375 / 1e6 + 200_000 * 3.75 / 1e6
    assert costs.cost_from_usage("gemini-3.8-flash", u) == pytest.approx(expected)


def test_cost_from_usage_survives_none_fields():
    assert costs.cost_from_usage("gemini-3.8-flash", usage()) == 0.0


def test_unknown_cache_price_is_charged_as_input():
    a = costs.request_cost("gemini-4-argon", 1_000_000, 0, cached_tokens=1_000_000)
    assert a == pytest.approx(2.0)


def test_unknown_model_has_clear_error():
    with pytest.raises(KeyError, match="PRICES"):
        costs.request_cost("gemini-9-unknown", 1, 1)


def test_usage_summary():
    s = costs.usage_summary("gemini-4-argon", usage(prompt_token_count=6000, thoughts_token_count=9000,
                                                     candidates_token_count=1200))
    assert s["cost_usd"] == pytest.approx(0.114) and s["thoughts_share"] == 0.88


def test_cache_break_even_formula_13_4():
    # розділ 13: 1 год -> 1,25 / 0,7125 ≈ 1,75; 8 год -> 4,75 / 0,7125 ≈ 6,7
    assert costs.cache_break_even("gemini-3.8-flash", hours=1) == pytest.approx(1.25 / 0.7125)
    assert costs.cache_break_even("gemini-3.8-flash", hours=8) == pytest.approx(6.667, abs=1e-3)
    # з 2027 року: кеш 0,075, зберігання 1,00 -> (0,75 + 8) / 0,675 ≈ 13
    p = costs.PRICES["gemini-3.8-flash"]
    try:
        costs.PRICES["gemini-3.8-flash"] = p._replace(cached=0.075)
        assert round(costs.cache_break_even("gemini-3.8-flash", 8, storage_per_hour=1.0)) == 13
    finally:
        costs.PRICES["gemini-3.8-flash"] = p
    assert costs.cache_break_even("gemini-4-argon", 1, storage_per_hour=1.0) == float("inf")


def test_cache_costs_cross_at_break_even():
    n_star = costs.cache_break_even("gemini-3.8-flash", hours=8)
    below = costs.cache_costs("gemini-3.8-flash", 200_000, int(n_star), hours=8)
    above = costs.cache_costs("gemini-3.8-flash", 200_000, int(n_star) + 1, hours=8)
    assert below[0] < below[1] and above[0] > above[1]
