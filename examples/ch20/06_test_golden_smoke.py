# Розділ 20. Оцінювання застосунків на Gemini – приклад 6 (рукопис: 20-otsiniuvannia.md, рядок 408)
# tests/test_golden_smoke.py – запускається на кожен pull request
import json
import pathlib
import pytest
from trembita.evals import classify_intent, paired_regression

ROOT = pathlib.Path(__file__).parent.parent / "evals"
CASES = [json.loads(line) for line in
         (ROOT / "golden.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
SMOKE = [c for c in CASES if "smoke" in c["tags"]]
# базова лінія по випадках, а не одне число: {"trk-017": true, "clm-044": false, ...}
BASELINE = json.loads((ROOT / "baseline_smoke.json").read_text(encoding="utf-8"))
RUNS_CRITICAL = 3         # критичні випадки – голосування більшістю з трьох прогонів

def passed(case: dict, runs: int = 1) -> bool:
    votes = sum(classify_intent(case["input"]) == case["expected_intent"] for _ in range(runs))
    return 2 * votes > runs

@pytest.fixture(scope="module")
def outcomes() -> dict[str, bool]:
    return {c["id"]: passed(c, RUNS_CRITICAL if "critical" in c["tags"] else 1) for c in SMOKE}

def test_critical_cases(outcomes):
    failed = [c["id"] for c in SMOKE if "critical" in c["tags"] and not outcomes[c["id"]]]
    assert not failed, f"Регресія в критичних випадках: {failed}"

def test_no_paired_regression(outcomes):
    r = paired_regression(BASELINE, outcomes)
    assert not r["regression"], (
        f"Значуща регресія: зламалося {r['b']}, виправилося {r['c']} "
        f"з {r['n']} випадків (p = {r['p']:.3f})")
