from datetime import date
from types import SimpleNamespace as NS

from google.genai import types

from trembita import assistant, pickup_guard as pg

ARGS = {"address": "м. Львів, вул. Зелена, 1", "date": "2026-11-02", "weight_kg": 5}


def make_guard():
    return pg.PickupGuard(pg.DemoBookingAPI(), pg.ListAudit(), today=lambda: date(2026, 10, 31))


def test_pickup_waits_without_operator():
    guard = make_guard()
    r = assistant.run_tool("create_pickup", ARGS, guard=guard)
    assert r["status"] == "awaiting_human_confirmation" and not guard.booking_api.created


def test_operator_confirms_or_rejects():
    guard = make_guard()
    ok = assistant.run_tool("create_pickup", ARGS, guard=guard, confirm=lambda n, a: True)
    assert ok["status"] == "створено" and len(guard.booking_api.created) == 1
    no = assistant.run_tool("create_pickup", ARGS, guard=guard, confirm=lambda n, a: False)
    assert no["status"] == "rejected" and len(guard.booking_api.created) == 1 and not guard.pending


def test_bad_calls_return_errors():
    assert "error" in assistant.run_tool("drop_database", {})
    assert "error" in assistant.run_tool("track_shipment", {"bad": 1})
    assert "error" in assistant.run_tool("create_pickup", {"address": "м. Львів, 1"})


class FakeModels:
    """Імітує generate_content: спершу просить інструмент, потім відповідає текстом."""
    def __init__(self):
        self.calls = 0

    def generate_content(self, model, contents, config):
        self.calls += 1
        if self.calls == 1:
            fc = types.FunctionCall(id="c1", name="track_shipment", args={"shipment_id": "SM-2610-0042"})
            content = types.Content(role="model", parts=[types.Part(function_call=fc)])
            return NS(candidates=[NS(content=content)], function_calls=[fc], text=None)
        fr = contents[-1].parts[0].function_response
        assert fr.id == "c1"
        content = types.Content(role="model", parts=[types.Part(text=f"Статус: {fr.response['status']}")])
        return NS(candidates=[NS(content=content)], function_calls=None, text=f"Статус: {fr.response['status']}")


def test_chat_turn_runs_tool_loop():
    client = NS(models=FakeModels())
    history = []
    answer = assistant.chat_turn(client, history, "Де SM-2610-0042?")
    assert answer == "Статус: у дорозі"
    assert [c.role for c in history] == ["user", "model", "user", "model"]


def test_chat_turn_handles_blocked_prompt():
    blocked = NS(candidates=None, prompt_feedback=NS(block_reason="SAFETY"), function_calls=None, text=None)
    client = NS(models=NS(generate_content=lambda **kw: blocked))
    assert "SAFETY" in assistant.chat_turn(client, [], "...")
