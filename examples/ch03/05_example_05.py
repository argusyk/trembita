# Розділ 3. Токени, мультимодальні токени й довгий контекст – приклад 5 (рукопис: 03-tokeny-kontekst.md, рядок 319)
from google.genai import types
from trembita.costs import cost_from_usage   # формула (3.7); ціни – у trembita/config.py

def log_usage(resp: types.GenerateContentResponse, model: str) -> None:
    u = resp.usage_metadata
    if u is None:                              # заблокований чи обірваний запит
        print("usage_metadata відсутнє")
        return
    by_mod = {(d.modality.name if d.modality else "?"): d.token_count
              for d in (u.prompt_tokens_details or [])}
    print(f"вхід={u.prompt_token_count} {by_mod} кеш={u.cached_content_token_count} "
          f"інструменти={u.tool_use_prompt_token_count} мислення={u.thoughts_token_count} "
          f"вихід={u.candidates_token_count} вартість={cost_from_usage(model, u):.4f} дол.")
