import pytest

pytest.importorskip("google.adk")
pytest.importorskip("a2a")

from trembita.agents import dispatcher, root_agent  # noqa: E402


def test_team_structure():
    assert root_agent is dispatcher
    assert {a.name for a in dispatcher.sub_agents} == {"tracker", "claim_pipeline", "customs"}
    assert dispatcher.tools[0].name == "tariff"         # агент як інструмент


def test_claim_pipeline_shape():
    pipeline = next(a for a in dispatcher.sub_agents if a.name == "claim_pipeline")
    gather, loop = pipeline.sub_agents
    assert [a.name for a in gather.sub_agents] == ["route_facts", "doc_facts"]
    assert loop.max_iterations == 3
