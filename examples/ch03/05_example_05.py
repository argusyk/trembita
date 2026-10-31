# Розділ 3. Токени, мультимодальні токени й довгий контекст – приклад 5 (рукопис: 03-tokeny-kontekst.md, рядок 318)
from dataclasses import dataclass
from google.genai import types

@dataclass
class Prices:                 # дол. за 1 млн токенів – з актуальної сторінки цін
    inp: float
    out: float
    cached: float

def request_cost(u: types.GenerateContentResponseUsageMetadata, p: Prices) -> float:
    prompt = u.prompt_token_count or 0
    cached = u.cached_content_token_count or 0
    out = (u.candidates_token_count or 0) + (u.thoughts_token_count or 0)
    return ((prompt - cached) * p.inp + cached * p.cached + out * p.out) / 1e6

def log_usage(resp: types.GenerateContentResponse, p: Prices) -> None:
    u = resp.usage_metadata
    by_mod = {(d.modality.name if d.modality else "?"): d.token_count
              for d in (u.prompt_tokens_details or [])}
    print(f"вхід={u.prompt_token_count} {by_mod} кеш={u.cached_content_token_count} "
          f"мислення={u.thoughts_token_count} вихід={u.candidates_token_count} "
          f"вартість={request_cost(u, p):.4f} дол.")
