# Chapter 1. What Is Gemini: Google DeepMind, the Ecosystem and a Running Example – example 2 (manuscript: 01-vstup-gemini.md, line 219)
if not response.candidates:                 # the prompt was blocked before reaching the model
    feedback = response.prompt_feedback
    print("blocked:", feedback.block_reason if feedback else "reason unknown")
else:
    candidate = response.candidates[0]
    print(candidate.finish_reason)          # FinishReason.STOP – natural ending
    if candidate.finish_reason == types.FinishReason.MAX_TOKENS:
        print("response truncated: increase max_output_tokens or lower the thinking level")

usage = response.usage_metadata
print("input:", usage.prompt_token_count)
print("output:", usage.candidates_token_count)
print("thinking:", usage.thoughts_token_count)
print("total:", usage.total_token_count)
