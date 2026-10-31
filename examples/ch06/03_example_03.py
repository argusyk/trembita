# Розділ 6. Родина моделей Gemini і відкриті моделі Gemma – приклад 3 (рукопис: 06-rodyna-modeley.md, рядок 171)
import logging

from google.genai import types

log = logging.getLogger("trembita.models")
AGING = {types.ModelStage.LEGACY, types.ModelStage.DEPRECATED}

def check_model_health(resp: types.GenerateContentResponse, requested: str) -> None:
    """Пише попередження, якщо модель старіє або відповіла не та, яку просили."""
    if resp.model_version and not resp.model_version.startswith(requested):
        log.warning("Запитували %s, відповіла %s", requested, resp.model_version)
    status = resp.model_status
    if status is None:          # поле не заповнюється на Agent Platform
        return
    if status.model_stage in AGING:
        log.warning("Модель %s на стадії %s, вимкнення: %s",
                    requested, status.model_stage.name, status.retirement_time)
