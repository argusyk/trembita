# Розділ 1. Що таке Gemini: Google DeepMind, екосистема й наскрізний приклад – приклад 2 (рукопис: 01-vstup-gemini.md, рядок 219)
if not response.candidates:                 # підказку заблоковано ще до моделі
    feedback = response.prompt_feedback
    print("заблоковано:", feedback.block_reason if feedback else "причина невідома")
else:
    candidate = response.candidates[0]
    print(candidate.finish_reason)          # FinishReason.STOP – природне завершення
    if candidate.finish_reason == types.FinishReason.MAX_TOKENS:
        print("відповідь обрізано: збільште max_output_tokens або знизьте рівень мислення")

usage = response.usage_metadata
print("вхід:", usage.prompt_token_count)
print("вихід:", usage.candidates_token_count)
print("мислення:", usage.thoughts_token_count)
print("разом:", usage.total_token_count)
