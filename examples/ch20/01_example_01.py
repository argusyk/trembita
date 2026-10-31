# Розділ 20. Оцінювання застосунків на Gemini – приклад 1 (рукопис: 20-otsiniuvannia.md, рядок 89)
import re
from collections import Counter

def tokens(s: str) -> list[str]:
    return re.findall(r"[\w'-]+", s.lower())        # \w у Python 3 розуміє кирилицю

def exact_match(pred: str, gold: str) -> bool:
    return tokens(pred) == tokens(gold)

def token_f1(pred: str, gold: str) -> float:
    p, g = tokens(pred), tokens(gold)
    common = sum((Counter(p) & Counter(g)).values())
    if not common:
        return 0.0
    prec, rec = common / len(p), common / len(g)
    return 2 * prec * rec / (prec + rec)

def per_class(preds: list[str], golds: list[str]) -> dict[str, tuple[float, float, float]]:
    """Влучність, повнота й F1 для кожного класу (формули 20.2 і 20.3)."""
    out = {}
    for c in sorted(set(golds) | set(preds)):
        tp = sum(p == c and g == c for p, g in zip(preds, golds))
        fp = sum(p == c and g != c for p, g in zip(preds, golds))
        fn = sum(p != c and g == c for p, g in zip(preds, golds))
        pr = tp / (tp + fp) if tp + fp else 0.0
        rc = tp / (tp + fn) if tp + fn else 0.0
        out[c] = (pr, rc, 2 * pr * rc / (pr + rc) if pr + rc else 0.0)
    return out
