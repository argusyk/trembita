# Розділ 6. Родина моделей Gemini і відкриті моделі Gemma – приклад 6 (рукопис: 06-rodyna-modeley.md, рядок 293)
from google.genai import errors

from trembita.config import MODEL_EMBED, MODEL_LITE, MODEL_MAIN, MODEL_SMART

def verify_models(min_input_tokens: int = 200_000) -> list[str]:
    """Перевіряє на старті, що закріплені моделі доступні; повертає перелік проблем."""
    problems = []
    for model_id in (MODEL_MAIN, MODEL_SMART, MODEL_LITE, MODEL_EMBED):
        try:
            m = client.models.get(model=model_id)
        except errors.APIError as e:          # 404 – модель зникла або недоступна ключу
            problems.append(f"{model_id}: {e.code}")
            continue
        if model_id != MODEL_EMBED and (m.input_token_limit or 0) < min_input_tokens:
            problems.append(f"{model_id}: контекст лише {m.input_token_limit}")
    return problems
