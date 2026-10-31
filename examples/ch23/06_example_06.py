# Розділ 23. Промислова експлуатація на Gemini Enterprise Agent Platform – приклад 6 (рукопис: 23-produkshn.md, рядок 298)
import json, logging, time
from opentelemetry import trace
from opentelemetry.trace import Status, StatusCode
from google.genai import types
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION

tracer = trace.get_tracer("trembita")
log = logging.getLogger("trembita.llm")


def usage_record(resp) -> dict:
    """Поля відповіді для журналу: версія, причина завершення, токени, рівень обслуговування."""
    u = resp.usage_metadata
    cand = resp.candidates[0] if resp.candidates else None
    return {
        "model_version": resp.model_version,
        "finish_reason": str(cand.finish_reason) if cand else "NO_CANDIDATES",
        "tokens_in": u.prompt_token_count if u else None,
        "tokens_out": u.candidates_token_count if u else None,
        "tokens_thoughts": u.thoughts_token_count if u else None,   # тарифікуються як вихідні
        "tokens_cached": u.cached_content_token_count if u else None,
        "traffic_type": str(u.traffic_type) if u else None,
    }
