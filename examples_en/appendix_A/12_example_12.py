# Appendix A. Laboratory Practicum – example 12 (manuscript: 90-appendix-a.md, line 623)
from trembita.evals import mcnemar_p, wilson

def compare(ok_a: list[bool], ok_b: list[bool]) -> dict:
    """ok_a[i], ok_b[i] – whether configurations A and B answered case i correctly."""
    n = len(ok_a)
    b = sum(x and not y for x, y in zip(ok_a, ok_b))   # only A is right
    c = sum(y and not x for x, y in zip(ok_a, ok_b))   # only B is right
    return {"acc_a": sum(ok_a) / n, "ci_a": wilson(sum(ok_a), n),
            "acc_b": sum(ok_b) / n, "ci_b": wilson(sum(ok_b), n),
            "b": b, "c": c, "p": mcnemar_p(b, c)}
