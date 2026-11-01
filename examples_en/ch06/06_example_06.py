# Chapter 6. The Gemini Model Family and the Open Gemma Models – example 6 (manuscript: 06-rodyna-modeley.md, line 307)
from google.genai import errors

from trembita.config import MODEL_EMBED, MODEL_FALLBACK, MODEL_LITE, MODEL_MAIN, MODEL_SMART

def verify_models(min_input_tokens: int = 200_000) -> list[str]:
    """Check at startup that the pinned models are available; return a list of problems."""
    problems = []
    for model_id in (MODEL_MAIN, MODEL_SMART, MODEL_LITE, MODEL_FALLBACK, MODEL_EMBED):
        try:
            m = client.models.get(model=model_id)
        except errors.APIError as e:          # 404 – the model is gone or unavailable to the key
            problems.append(f"{model_id}: {e.code}")
            continue
        if model_id != MODEL_EMBED and (m.input_token_limit or 0) < min_input_tokens:
            problems.append(f"{model_id}: context only {m.input_token_limit}")
    return problems
