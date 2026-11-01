# Chapter 12. Grounding and Built-in Tools – example 2 (manuscript: 12-zazemlennia.md, line 76)
from collections import defaultdict

def add_citations(resp) -> str:
    """Inserts [1], [2]... after fragments confirmed by sources."""
    cand = resp.candidates[0] if resp.candidates else None
    if cand is None or cand.content is None:
        return ""
    meta = cand.grounding_metadata                   # None if the model did not search
    by_part = defaultdict(list)                      # segments grouped by part_index
    for sup in (meta.grounding_supports or []) if meta else []:
        if sup.segment and sup.grounding_chunk_indices:
            by_part[sup.segment.part_index or 0].append(sup)
    out = []
    for idx, part in enumerate(cand.content.parts or []):
        if not part.text or part.thought:
            continue
        raw = part.text.encode("utf-8")              # offsets are in bytes from the start of the part!
        # from end to start, so that insertions do not shift positions not yet processed
        for sup in sorted(by_part[idx], key=lambda s: s.segment.end_index or 0, reverse=True):
            end = sup.segment.end_index or 0
            marks = "".join(f"[{i + 1}]" for i in sup.grounding_chunk_indices)
            raw = raw[:end] + marks.encode("utf-8") + raw[end:]
        out.append(raw.decode("utf-8"))
    return "".join(out)
