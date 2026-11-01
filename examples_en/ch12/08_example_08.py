# Chapter 12. Grounding and Built-in Tools – example 8 (manuscript: 12-zazemlennia.md, line 366)
_NUMBER = re.compile(r"[-+]?\d+(?:[.,]\d+)?")      # continuation of trembita/planning.py

def parse_result_line(output: str) -> tuple[float, float] | None:
    """(weight_kg, volume_m3) from the last "RESULT <weight> <volume>" line, or None."""
    lines = [ln.strip() for ln in str(output).splitlines() if ln.strip().upper().startswith("RESULT")]
    if not lines:
        return None
    nums = _NUMBER.findall(lines[-1][len("RESULT"):].replace("m3", " ").replace("m³", " "))
    if len(nums) < 2:
        return None
    kg, m3 = (float(n.replace(",", ".")) for n in nums[:2])   # "2500,0" and "2500 kg" too
    if kg <= 0 or m3 < 0:
        return None
    return kg, m3

def web_sources(resp) -> list[dict]:
    """Search sources from grounding_metadata (empty if the model did not search)."""
    cands = getattr(resp, "candidates", None) or []
    meta = getattr(cands[0], "grounding_metadata", None) if cands else None
    out = []
    for c in (getattr(meta, "grounding_chunks", None) or []):
        web = getattr(c, "web", None)
        if web is not None and web.uri:
            out.append({"uri": web.uri, "title": web.title or "", "domain": web.domain or ""})
    return out

def _assemble(origin: str, destination: str, places, news, weight) -> dict:
    runs = code_outputs(weight)                                  # only runs with OUTCOME_OK
    parsed = parse_result_line(runs[-1]) if runs else None      # the last successful attempt
    kg, m3 = parsed or (None, None)
    return {
        "crossings": response_text(places), "border_news": response_text(news),
        "sources": web_sources(news),
        "billable_kg": kg, "volume_m3": m3,
        "tariff": get_tariff(origin, destination, kg, m3) if kg else None,
        "issues": [] if parsed else ["Could not calculate the weight – clarify the cargo description"],
        "status": "draft"}               # the plan is a draft; the dispatcher decides
