# Chapter 20. Evaluating Gemini Applications – example 6 (manuscript: 20-otsiniuvannia.md, line 408)
# tests/test_golden_smoke.py – runs on every pull request
import json
import pathlib
import pytest
from trembita.evals import classify_intent, paired_regression

ROOT = pathlib.Path(__file__).parent.parent / "evals"
CASES = [json.loads(line) for line in
         (ROOT / "golden.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
SMOKE = [c for c in CASES if "smoke" in c["tags"]]
# per-case baseline rather than a single number: {"trk-017": true, "clm-044": false, ...}
BASELINE = json.loads((ROOT / "baseline_smoke.json").read_text(encoding="utf-8"))
RUNS_CRITICAL = 3         # critical cases: majority vote over three runs

def passed(case: dict, runs: int = 1) -> bool:
    votes = sum(classify_intent(case["input"]) == case["expected_intent"] for _ in range(runs))
    return 2 * votes > runs

@pytest.fixture(scope="module")
def outcomes() -> dict[str, bool]:
    return {c["id"]: passed(c, RUNS_CRITICAL if "critical" in c["tags"] else 1) for c in SMOKE}

def test_critical_cases(outcomes):
    failed = [c["id"] for c in SMOKE if "critical" in c["tags"] and not outcomes[c["id"]]]
    assert not failed, f"Regression in critical cases: {failed}"

def test_no_paired_regression(outcomes):
    r = paired_regression(BASELINE, outcomes)
    assert not r["regression"], (
        f"Significant regression: {r['b']} broke, {r['c']} fixed "
        f"out of {r['n']} cases (p = {r['p']:.3f})")
