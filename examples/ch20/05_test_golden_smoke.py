# Розділ 20. Оцінювання застосунків на Gemini – приклад 5 (рукопис: 20-otsiniuvannia.md, рядок 392)
# tests/test_golden_smoke.py – запускається на кожен pull request
import json
import pathlib
import pytest
from trembita.evals import classify_intent, wilson

ROOT = pathlib.Path(__file__).parent.parent / "evals"
CASES = [json.loads(line) for line in
         (ROOT / "golden.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
SMOKE = [c for c in CASES if "smoke" in c["tags"]]
BASELINE = json.loads((ROOT / "baseline.json").read_text(encoding="utf-8"))
TOLERANCE = 0.03          # допуск на шум недетермінованої моделі

@pytest.fixture(scope="module")
def outcomes() -> dict[str, bool]:
    return {c["id"]: classify_intent(c["input"]) == c["expected_intent"] for c in SMOKE}

def test_critical_cases(outcomes):
    failed = [c["id"] for c in SMOKE if "critical" in c["tags"] and not outcomes[c["id"]]]
    assert not failed, f"Регресія в критичних випадках: {failed}"

def test_accuracy_vs_baseline(outcomes):
    k, n = sum(outcomes.values()), len(outcomes)
    low, high = wilson(k, n)
    assert k / n >= BASELINE["smoke_accuracy"] - TOLERANCE, (
        f"Точність {k / n:.3f} (95 % ДІ {low:.3f}-{high:.3f}) "
        f"нижча за базову {BASELINE['smoke_accuracy']:.3f}")
