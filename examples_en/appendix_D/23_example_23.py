# Appendix D. Code Recipes – example 23 (manuscript: 93-appendix-d.md, line 444)
def add_citations(resp) -> str:
    text = resp.text or ""
    meta = resp.candidates[0].grounding_metadata if resp.candidates else None
    if not meta or not meta.grounding_supports:
        return text
    raw = text.encode("utf-8")                   # indices are in bytes
    # from the end to the beginning, so that insertions do not shift positions not yet processed
    for sup in sorted(meta.grounding_supports, key=lambda s: s.segment.end_index, reverse=True):
        if sup.segment and sup.grounding_chunk_indices:
            marks = "".join(f"[{i + 1}]" for i in sup.grounding_chunk_indices)
            end = sup.segment.end_index
            raw = raw[:end] + marks.encode("utf-8") + raw[end:]
    return raw.decode("utf-8")
