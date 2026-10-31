from datetime import date

import pytest

from trembita import pickup_guard as pg

TODAY = date(2026, 10, 31)


class Clock:
    def __init__(self):
        self.t = 1000.0

    def __call__(self):
        return self.t


@pytest.fixture
def env():
    clock, api, audit = Clock(), pg.DemoBookingAPI(), pg.ListAudit()
    day = {"today": TODAY}
    guard = pg.PickupGuard(api, audit, clock=clock, today=lambda: day["today"])
    return guard, api, audit, clock, day


@pytest.mark.parametrize("address,city", [
    ("м. Львів, вул. Зелена, 1", "львів"),
    ("ЛЬВІВ, вул. Зелена, 1", "львів"),
    ("місто Київ, вул. Пухівська, 4", "київ"),
    ("м.Ужгород, вул. Собранецька, 160", "ужгород"),
    ("Одеса, вул. Київська, 5", None),          # «Київська» не робить Одесу Києвом
    ("вул. Зелена, 1, Львів", None),            # місто має бути першим
    ("Львівська обл., с. Сокільники", None),
])
def test_city_of_exact(address, city):
    assert pg.city_of(address) == city


def test_validation_messages():
    assert pg.validate_pickup("м. Львів, вул. Зелена, 1", "2026-10-31", 10, today=TODAY) == []
    errs = pg.validate_pickup("Одеса, вул. Київська, 5", "31.12.2019", "x", today=TODAY)
    assert len(errs) == 3 and "РРРР-ММ-ДД" in errs[1]
    assert pg.validate_pickup("м. Львів, 1", "2019-12-31", 10, today=TODAY) == ["дата в минулому"]
    assert pg.validate_pickup("м. Львів, 1", "2026-11-01", pg.MAX_PICKUP_KG + 1, today=TODAY)
    assert pg.validate_pickup("м. Львів, 1", "2026-11-01", 0, today=TODAY)


def test_propose_then_confirm_creates_once(env):
    guard, api, audit, clock, _ = env
    p = guard.propose("м. Львів, вул. Зелена, 1", "2026-11-02", 840)
    assert p["status"] == "awaiting_human_confirmation" and not api.created
    r = guard.confirm(p["token"], "Ірина")
    assert r["status"] == "створено" and r["pickup_id"].startswith("PU-1102-")
    assert guard.confirm(p["token"], "Ірина")["status"] == "error"    # повтор не створить дубль
    assert len(api.created) == 1
    assert audit.records[-1]["by"] == "Ірина"


def test_unknown_token(env):
    guard, api, *_ = env
    assert guard.confirm("nope", "Ірина") == {"status": "error", "error": "невідома або вже оброблена заявка"}
    assert not api.created


def test_token_expires(env):
    guard, api, audit, clock, _ = env
    p = guard.propose("м. Київ, вул. Пухівська, 4", "2026-11-02", 10)
    clock.t += pg.TOKEN_TTL_S + 1
    r = guard.confirm(p["token"], "Ірина")
    assert r["status"] == "error" and "термін" in r["error"] and not api.created
    assert audit.records[-1]["result"] == "expired"


def test_confirm_revalidates(env):
    guard, api, audit, clock, day = env
    p = guard.propose("м. Київ, вул. Пухівська, 4", "2026-10-31", 10)
    day["today"] = date(2026, 11, 1)                     # поки чекали, дата стала минулою
    assert guard.confirm(p["token"], "Ірина")["status"] == "rejected" and not api.created


def test_reject_and_tokens_unique(env):
    guard, api, *_ = env
    a = guard.propose("м. Львів, вул. Зелена, 1", "2026-11-02", 10)
    b = guard.propose("м. Львів, вул. Зелена, 1", "2026-11-02", 10)
    assert a["token"] != b["token"] and len(a["token"]) == 16
    assert guard.reject(a["token"], "Ірина")["status"] == "rejected"
    assert guard.confirm(a["token"], "Ірина")["status"] == "error"


def test_as_tool_is_bound_and_named(env):
    guard, *_ = env
    tool = guard.as_tool()
    assert tool.__name__ == "create_pickup"
    assert tool("м. Львів, вул. Зелена, 1", "2026-11-02", 10)["token"] in guard.pending
