# Розділ 1. Що таке Gemini: Google DeepMind, екосистема й наскрізний приклад – приклад 3 (рукопис: 01-vstup-gemini.md, рядок 236)
candidate = response.candidates[0]
print(candidate.finish_reason)        # FinishReason.STOP – природне завершення

usage = response.usage_metadata
print("вхід:", usage.prompt_token_count)
print("вихід:", usage.candidates_token_count)
print("мислення:", usage.thoughts_token_count)
print("разом:", usage.total_token_count)
