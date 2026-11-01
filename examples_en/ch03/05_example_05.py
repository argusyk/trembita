# Chapter 3. Tokens, Multimodal Tokens and Long Context – example 5 (manuscript: 03-tokeny-kontekst.md, line 319)
from google.genai import types
from trembita.costs import cost_from_usage   # formula (3.7); prices are in trembita/config.py

def log_usage(resp: types.GenerateContentResponse, model: str) -> None:
    u = resp.usage_metadata
    if u is None:                              # a blocked or interrupted request
        print("usage_metadata is missing")
        return
    by_mod = {(d.modality.name if d.modality else "?"): d.token_count
              for d in (u.prompt_tokens_details or [])}
    print(f"input={u.prompt_token_count} {by_mod} cache={u.cached_content_token_count} "
          f"tools={u.tool_use_prompt_token_count} thinking={u.thoughts_token_count} "
          f"output={u.candidates_token_count} cost={cost_from_usage(model, u):.4f} USD")
