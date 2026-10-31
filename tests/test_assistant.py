from types import SimpleNamespace as NS

from google.genai import types

from trembita import assistant


def test_effects_need_confirmation():
    args = {"address": "Київ", "date": "2026-11-01", "weight_kg": 5}
    assert "error" in assistant.run_tool("create_pickup", args)
    assert assistant.run_tool("create_pickup", args, confirm=lambda n, a: True)["status"] == "створено"
    assert "error" in assistant.run_tool("drop_database", {})
    assert "error" in assistant.run_tool("track_shipment", {"bad": 1})


class FakeModels:
    """Імітує generate_content: спершу просить інструмент, потім відповідає текстом."""
    def __init__(self):
        self.calls = 0

    def generate_content(self, model, contents, config):
        self.calls += 1
        if self.calls == 1:
            fc = types.FunctionCall(name="track_shipment", args={"shipment_id": "SM-2610-0042"})
            content = types.Content(role="model", parts=[types.Part(function_call=fc)])
            return NS(candidates=[NS(content=content)], function_calls=[fc], text=None)
        last = contents[-1].parts[0].function_response.response
        content = types.Content(role="model", parts=[types.Part(text=f"Статус: {last['status']}")])
        return NS(candidates=[NS(content=content)], function_calls=None, text=f"Статус: {last['status']}")


def test_chat_turn_runs_tool_loop():
    client = NS(models=FakeModels())
    history = []
    answer = assistant.chat_turn(client, history, "Де SM-2610-0042?")
    assert answer == "Статус: у дорозі"
    assert [c.role for c in history] == ["user", "model", "user", "model"]
