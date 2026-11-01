# Chapter 6. The Gemini Model Family and the Open Gemma Models – example 3 (manuscript: 06-rodyna-modeley.md, line 185)
import logging

from google.genai import types

log = logging.getLogger("trembita.models")
AGING = {types.ModelStage.LEGACY, types.ModelStage.DEPRECATED}

def check_model_health(resp: types.GenerateContentResponse, requested: str) -> None:
    """Log a warning if the model is aging or a different model answered than requested."""
    if resp.model_version and not resp.model_version.startswith(requested):
        log.warning("Requested %s, answered by %s", requested, resp.model_version)
    status = resp.model_status
    if status is None:          # the field is not filled in on Agent Platform
        return
    if status.model_stage in AGING:
        log.warning("Model %s is at stage %s, retirement: %s",
                    requested, status.model_stage.name, status.retirement_time)
