# Appendix D. Code Recipes – example 38 (manuscript: 93-appendix-d.md, line 775)
BLOCKED = {types.FinishReason.SAFETY, types.FinishReason.PROHIBITED_CONTENT,
           types.FinishReason.BLOCKLIST, types.FinishReason.SPII}

def safe_text(resp: types.GenerateContentResponse) -> str:
    fb = resp.prompt_feedback
    if fb is not None and fb.block_reason:           # the request was rejected before generation
        return f"The request was blocked ({fb.block_reason.name}). Please contact a dispatcher."
    if not resp.candidates:
        return "The response is empty."
    cand = resp.candidates[0]
    if cand.finish_reason in BLOCKED:                # a filter stopped the generation
        return "The response was blocked by a safety filter."
    if cand.finish_reason == types.FinishReason.MAX_TOKENS:
        print("Warning: the response was truncated, increase max_output_tokens")
    return resp.text or ""
