# Chapter 5. Safety and Alignment at Google DeepMind – example 2 (manuscript: 05-bezpeka-vyrivniuvannia.md, line 121)
def explain_block(resp: types.GenerateContentResponse) -> str | None:
    """Return a description of the block, or None if the response is normal."""
    fb = resp.prompt_feedback
    if fb is not None and fb.block_reason is not None:
        return f"prompt blocked: {fb.block_reason.name}"
    if not resp.candidates:
        return "no candidates"
    cand = resp.candidates[0]
    if cand.finish_reason == types.FinishReason.SAFETY:
        hits = [r.category.name for r in (cand.safety_ratings or []) if r.blocked]
        return f"response blocked by filter: {', '.join(hits) or '?'}"
    if cand.finish_reason in (types.FinishReason.PROHIBITED_CONTENT,
                              types.FinishReason.BLOCKLIST,
                              types.FinishReason.SPII):
        return f"response stopped: {cand.finish_reason.name}"
    return None

reason = explain_block(resp)
if reason:
    print("Could not answer automatically; handing over to a dispatcher.", reason)
else:
    print(resp.text)
