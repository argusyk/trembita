from datetime import date
from types import SimpleNamespace as NS

import pytest
from google.genai import types

from trembita import documents, planning
from trembita.schemas import CargoItem, Waybill

TODAY = date(2026, 10, 31)


def wb(**kw):
    base = dict(number="CMR-2610-17", date="2026-10-26", sender="ТОВ «Смерека»", consignee="Kovacs Kft.",
                origin="Львів", destination="Ніредьгаза",
                items=[CargoItem(name="меблі", packages=12, weight_kg=840)])
    return Waybill(**{**base, **kw})


@pytest.mark.parametrize("number", ["CMR-2610-17", "UA 0042517", "АА 123456", "118/26", "№ 0042517", "PL1234567"])
def test_cmr_number_accepts_ukrainian_and_foreign(number):
    assert documents.looks_like_cmr_number(number)


@pytest.mark.parametrize("number", ["ABC", "??", "немає", "1"])
def test_cmr_number_rejects_garbage(number):
    assert not documents.looks_like_cmr_number(number)


def test_check_waybill_clean_and_issues():
    assert documents.check_waybill(wb(), 840, today=TODAY) == []
    issues = documents.check_waybill(wb(date="2026-12-01", sender="", notes="графа 11 у плямі"), 8400, today=TODAY)
    assert any("майбутнього" in i for i in issues) and any("8400" in i for i in issues)
    assert any("Порожні" in i for i in issues) and any("сумнівні" in i for i in issues)
    assert any("РРРР-ММ-ДД" in i for i in documents.check_waybill(wb(date="26.10.2026"), today=TODAY))
    assert documents.check_waybill(wb(), 0, today=TODAY) == []                # 0 – «не заявлено»


def test_parse_waybill_handles_none_and_text():
    good = wb()
    assert documents.parse_waybill(NS(parsed=good)) is good
    assert documents.parse_waybill(NS(parsed=None, text=good.model_dump_json())) == good
    assert documents.parse_waybill(NS(parsed=None, text=None)) is None
    assert documents.parse_waybill(NS(parsed=None, text='{"number": 1')) is None


def test_read_cmr_with_fake_client():
    ok = NS(models=NS(generate_content=lambda **kw: NS(parsed=wb())))
    w, issues = documents.read_cmr(b"jpeg", 840, client=ok)
    assert w.number == "CMR-2610-17" and issues == []
    blocked = NS(models=NS(generate_content=lambda **kw: NS(parsed=None, text=None)))
    w, issues = documents.read_cmr(b"jpeg", client=blocked)
    assert w is None and "ручний" in issues[0]


@pytest.mark.parametrize("out,expected", [
    ("V = 10\nRESULT 2500 7.2", (2500.0, 7.2)),
    ("RESULT 2500,0 7,2", (2500.0, 7.2)),
    ("RESULT 2500 кг 7.2 м3", (2500.0, 7.2)),
    ("RESULT 1 1\nпроміжне\nresult 1800.5 0", (1800.5, 0.0)),
    ("RESULT 2500", None),
    ("немає рядка", None),
    ("RESULT -5 1", None),
])
def test_parse_result_line(out, expected):
    assert planning.parse_result_line(out) == expected


def code_part(output, ok=True):
    outcome = types.Outcome.OUTCOME_OK if ok else types.Outcome.OUTCOME_FAILED
    return types.Part(code_execution_result=types.CodeExecutionResult(outcome=outcome, output=output))


def test_response_helpers_survive_missing_metadata():
    empty = NS(candidates=None, text=None)
    assert planning.code_outputs(empty) == [] and planning.web_sources(empty) == []
    assert planning.response_text(empty) == ""
    no_meta = NS(candidates=[NS(content=None, grounding_metadata=None)])
    assert planning.web_sources(no_meta) == [] and planning.code_outputs(no_meta) == []
    meta = types.GroundingMetadata(grounding_chunks=[
        types.GroundingChunk(web=types.GroundingChunkWeb(uri="https://dpsu.gov.ua/x", title="ДПСУ", domain="dpsu.gov.ua")),
        types.GroundingChunk()])
    assert planning.web_sources(NS(candidates=[NS(grounding_metadata=meta)]))[0]["domain"] == "dpsu.gov.ua"
    content = types.Content(role="model", parts=[code_part("RESULT 1 1"), code_part("boom", ok=False),
                                                 code_part("RESULT 2500 7,2")])
    assert planning.code_outputs(NS(candidates=[NS(content=content)])) == ["RESULT 1 1", "RESULT 2500 7,2"]


def test_plan_delivery_with_fake_client():
    content = types.Content(role="model", parts=[code_part("RESULT 2500 7,2")])
    replies = iter([NS(text="Краківець", candidates=[]),
                    NS(text="Черга 6 год", candidates=[NS(grounding_metadata=None)]),
                    NS(text=None, candidates=[NS(content=content)])])
    client = NS(models=NS(generate_content=lambda **kw: next(replies)))
    plan = planning.plan_delivery("Львів", "Київ", "6 палет", client=client)
    assert plan["billable_kg"] == 2500.0 and plan["tariff"]["price_uah"] == 16250.0
    assert plan["sources"] == [] and plan["status"] == "draft" and plan["issues"] == []
