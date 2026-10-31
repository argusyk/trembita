# Розділ 12. Заземлення та вбудовані інструменти – приклад 2 (рукопис: 12-zazemlennia.md, рядок 75)
def add_citations(resp) -> str:
    """Вставляє [1], [2]... після фрагментів, підтверджених джерелами."""
    meta = resp.candidates[0].grounding_metadata
    raw = resp.text.encode("utf-8")              # індекси сегментів – у байтах!
    if not meta or not meta.grounding_supports:
        return resp.text
    # з кінця до початку, щоб вставки не зсували ще не оброблені позиції
    supports = sorted(meta.grounding_supports, key=lambda s: s.segment.end_index, reverse=True)
    for sup in supports:
        if not sup.grounding_chunk_indices:
            continue
        marks = "".join(f"[{i + 1}]" for i in sup.grounding_chunk_indices)
        end = sup.segment.end_index
        raw = raw[:end] + marks.encode("utf-8") + raw[end:]
    return raw.decode("utf-8")
