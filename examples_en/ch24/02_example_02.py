# Chapter 24. Responsible AI: Bias, Fairness and Impact – example 2 (manuscript: 24-vidpovidalnyy-shi.md, line 159)
from collections import Counter


def group_rates(records: list[dict], group: str) -> dict:
    """records: {"group": "uk" | "en", "y": 0 | 1 (audit), "pred": 0 | 1 (Trembita)}"""
    c = Counter((r["y"], r["pred"]) for r in records if r["group"] == group)
    tp, fn, fp, tn = c[(1, 1)], c[(1, 0)], c[(0, 1)], c[(0, 0)]
    n = tp + fn + fp + tn
    return {
        "base_rate": (tp + fn) / n,
        "selection": (tp + fp) / n,      # demographic parity
        "tpr": tp / (tp + fn),           # equal opportunity
        "fpr": fp / (fp + tn),           # the other half of equalized odds
        "ppv": tp / (tp + fp),           # predictive parity (calibration)
    }


def fairness_report(records: list[dict], a: str = "en", b: str = "uk") -> dict:
    ra, rb = group_rates(records, a), group_rates(records, b)
    return {
        "disparate_impact": rb["selection"] / ra["selection"],   # reference: at least 0.8
        "tpr_gap": ra["tpr"] - rb["tpr"],
        "fpr_gap": ra["fpr"] - rb["fpr"],
        "ppv_gap": ra["ppv"] - rb["ppv"],
    }
