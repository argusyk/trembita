# Chapter 7. The Gemini API and the Google Gen AI SDK – example 4 (manuscript: 07-api.md, line 188)
from google.genai import types

# explain_block is from Section 5.3: request blocked, empty candidates, response filter


def describe(resp: types.GenerateContentResponse) -> str:
    """Returns the response text or a clear explanation of why there is none."""
    blocked = explain_block(resp)                    # 1. Request or response blocked
    if blocked:                                      #    (including candidates = None or [])
        return f"[{blocked}]"

    cand = resp.candidates[0]                        # now a candidate surely exists
    reason = cand.finish_reason                      # 2. Why the model stopped
    if reason == types.FinishReason.MAX_TOKENS:
        print("Warning: the response was cut off, increase max_output_tokens")
    elif reason not in (types.FinishReason.STOP, None):
        return f"[response stopped: {reason.name}]"

    u = resp.usage_metadata                          # 3. Token accounting (may be None)
    if u is not None:
        print(f"input={u.prompt_token_count} cache={u.cached_content_token_count} "
              f"output={u.candidates_token_count} thoughts={u.thoughts_token_count} "
              f"total={u.total_token_count}")
    return resp.text or "[no text parts]"           # 4. Only now, the text
