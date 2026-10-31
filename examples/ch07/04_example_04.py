# Розділ 7. Gemini API і Google Gen AI SDK – приклад 4 (рукопис: 07-api.md, рядок 188)
from google.genai import types

# explain_block – з підрозділу 5.3: блокування запиту, порожні candidates, фільтр відповіді


def describe(resp: types.GenerateContentResponse) -> str:
    """Повертає текст відповіді або зрозуміле пояснення, чому його немає."""
    blocked = explain_block(resp)                    # 1. Запит чи відповідь заблоковано
    if blocked:                                      #    (зокрема candidates = None або [])
        return f"[{blocked}]"

    cand = resp.candidates[0]                        # тепер кандидат точно є
    reason = cand.finish_reason                      # 2. Чому модель зупинилася
    if reason == types.FinishReason.MAX_TOKENS:
        print("Увага: відповідь обрізано, збільште max_output_tokens")
    elif reason not in (types.FinishReason.STOP, None):
        return f"[відповідь зупинено: {reason.name}]"

    u = resp.usage_metadata                          # 3. Облік токенів (може бути None)
    if u is not None:
        print(f"вхід={u.prompt_token_count} кеш={u.cached_content_token_count} "
              f"вихід={u.candidates_token_count} думки={u.thoughts_token_count} "
              f"разом={u.total_token_count}")
    return resp.text or "[текстових частин немає]"  # 4. Лише тепер – текст
