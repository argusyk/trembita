# Розділ 24. Відповідальний ШІ: упередженість, справедливість і вплив – приклад 2 (рукопис: 24-vidpovidalnyy-shi.md, рядок 155)
from collections import Counter


def group_rates(records: list[dict], group: str) -> dict:
    """records: {"group": "uk" | "en", "y": 0 | 1 (аудит), "pred": 0 | 1 («Трембіта»)}"""
    c = Counter((r["y"], r["pred"]) for r in records if r["group"] == group)
    tp, fn, fp, tn = c[(1, 1)], c[(1, 0)], c[(0, 1)], c[(0, 0)]
    n = tp + fn + fp + tn
    return {
        "base_rate": (tp + fn) / n,
        "selection": (tp + fp) / n,      # демографічний паритет
        "tpr": tp / (tp + fn),           # рівність можливостей
        "fpr": fp / (fp + tn),           # друга половина рівних шансів
        "ppv": tp / (tp + fp),           # калібрування за позитивним прогнозом
    }


def fairness_report(records: list[dict], a: str = "en", b: str = "uk") -> dict:
    ra, rb = group_rates(records, a), group_rates(records, b)
    return {
        "disparate_impact": rb["selection"] / ra["selection"],   # орієнтир: не менше 0,8
        "tpr_gap": ra["tpr"] - rb["tpr"],
        "fpr_gap": ra["fpr"] - rb["fpr"],
        "ppv_gap": ra["ppv"] - rb["ppv"],
    }
