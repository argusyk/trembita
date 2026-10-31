import re
import warnings
from types import SimpleNamespace as NS

import pytest

pytest.importorskip("google.adk")
pytest.importorskip("a2a")

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    from trembita.agents import dispatcher, root_agent, tariff_agent  # noqa: E402
    from trembita.agents import claims as claim_mod  # noqa: E402
    from trembita.agents import tracker as tracker_mod  # noqa: E402
from trembita.config import MODEL_LITE, MODEL_MAIN, MODEL_SMART  # noqa: E402

TEMPLATE = re.compile(r"(?<![\$\{\\]){+([^{}]*)}+")      # як у ADK _instructions_utils


def walk(agent):
    yield agent
    for sub in getattr(agent, "sub_agents", []) or []:
        yield from walk(sub)


def required_vars(agent) -> set[str]:
    instr = agent.instruction if isinstance(getattr(agent, "instruction", None), str) else ""
    names = {m.strip() for m in TEMPLATE.findall(instr)}
    return {n for n in names if not n.endswith("?") and not n.startswith("artifact.")}


def test_team_structure_and_models():
    assert root_agent is dispatcher
    assert {a.name for a in dispatcher.sub_agents} == {"tracker", "claim_pipeline", "customs"}
    assert [getattr(t, "name", None) for t in dispatcher.tools] == ["tariff", None]
    assert dispatcher.tools[1].__name__ == "register_claim"
    assert dispatcher.model == MODEL_MAIN and tariff_agent.model == MODEL_LITE
    smart = {a.name for a in walk(dispatcher) if getattr(a, "model", None) == MODEL_SMART}
    assert smart <= {"drafter", "reviewer"}


def test_claim_pipeline_shape():
    pipeline = next(a for a in dispatcher.sub_agents if a.name == "claim_pipeline")
    gather, loop = pipeline.sub_agents
    assert [a.name for a in gather.sub_agents] == ["route_facts", "doc_facts"]
    assert loop.max_iterations == 3


def test_every_required_state_var_has_a_writer():
    """Кожна обов'язкова {змінна} має джерело: output_key агента, що працює раніше, або інструмент."""
    writers = {a.output_key for a in walk(dispatcher) if getattr(a, "output_key", None)}
    writers |= set(claim_mod.CLAIM_KEYS)          # пише register_claim
    for agent in walk(dispatcher):
        missing = required_vars(agent) - writers
        assert not missing, f"{agent.name}: немає джерела для {missing}"
    assert not required_vars(claim_mod.route_facts) and not required_vars(claim_mod.doc_facts)


def test_register_claim_writes_state():
    ctx = NS(state={})
    assert claim_mod.register_claim("Розбита плитка, SM-2610-0230", "", ctx) == {"status": "ok"}
    assert ctx.state["claim_text"].startswith("Розбита") and ctx.state["cmr_text"]


def test_partner_tracker_is_separate_and_read_only():
    partner = tracker_mod.partner_tracker_agent
    assert partner is not tracker_mod.tracker_agent and partner.parent_agent is None
    names = {getattr(t, "__name__", getattr(t, "name", "")) for t in partner.tools}
    assert names == {"track_for_partner"} and partner.output_key is None
    ctx = NS(state={})
    assert "error" in tracker_mod.track_for_partner("SM-2610-0042", ctx)          # без автентифікації
    ctx.state[tracker_mod.PARTNER_KEY] = "dunai-cargo"
    assert tracker_mod.track_for_partner("sm-2610-0042", ctx)["status"] == "у дорозі"
    assert "недоступне" in tracker_mod.track_for_partner("SM-2610-0117", ctx)["error"]
