# Розділ 12. Заземлення та вбудовані інструменти – приклад 2 (рукопис: 12-zazemlennia.md, рядок 76)
from collections import defaultdict

def add_citations(resp) -> str:
    """Вставляє [1], [2]... після фрагментів, підтверджених джерелами."""
    cand = resp.candidates[0] if resp.candidates else None
    if cand is None or cand.content is None:
        return ""
    meta = cand.grounding_metadata                   # None, якщо модель не шукала
    by_part = defaultdict(list)                      # сегменти, згруповані за part_index
    for sup in (meta.grounding_supports or []) if meta else []:
        if sup.segment and sup.grounding_chunk_indices:
            by_part[sup.segment.part_index or 0].append(sup)
    out = []
    for idx, part in enumerate(cand.content.parts or []):
        if not part.text or part.thought:
            continue
        raw = part.text.encode("utf-8")              # зсуви – у байтах від початку частини!
        # з кінця до початку, щоб вставки не зсували ще не оброблені позиції
        for sup in sorted(by_part[idx], key=lambda s: s.segment.end_index or 0, reverse=True):
            end = sup.segment.end_index or 0
            marks = "".join(f"[{i + 1}]" for i in sup.grounding_chunk_indices)
            raw = raw[:end] + marks.encode("utf-8") + raw[end:]
        out.append(raw.decode("utf-8"))
    return "".join(out)
