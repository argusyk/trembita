# Додаток А. Практикум – приклад 11 (рукопис: 90-dodatok-a.md, рядок 554)
from trembita.evals import mcnemar_p, wilson

def compare(ok_a: list[bool], ok_b: list[bool]) -> dict:
    """ok_a[i], ok_b[i] – чи правильно відповіли конфігурації A і B на випадок i."""
    n = len(ok_a)
    b = sum(x and not y for x, y in zip(ok_a, ok_b))   # права лише A
    c = sum(y and not x for x, y in zip(ok_a, ok_b))   # права лише B
    return {"acc_a": sum(ok_a) / n, "ci_a": wilson(sum(ok_a), n),
            "acc_b": sum(ok_b) / n, "ci_b": wilson(sum(ok_b), n),
            "b": b, "c": c, "p": mcnemar_p(b, c)}
