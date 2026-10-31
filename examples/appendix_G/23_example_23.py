# Додаток Г. Довідник рецептів коду – приклад 23 (рукопис: 93-dodatok-g.md, рядок 439)
def add_citations(resp) -> str:
    meta = resp.candidates[0].grounding_metadata
    if not meta or not meta.grounding_supports:
        return resp.text
    raw = resp.text.encode("utf-8")              # індекси – у байтах
    # з кінця до початку, щоб вставки не зсували ще не оброблені позиції
    for sup in sorted(meta.grounding_supports, key=lambda s: s.segment.end_index, reverse=True):
        if sup.grounding_chunk_indices:
            marks = "".join(f"[{i + 1}]" for i in sup.grounding_chunk_indices)
            end = sup.segment.end_index
            raw = raw[:end] + marks.encode("utf-8") + raw[end:]
    return raw.decode("utf-8")
