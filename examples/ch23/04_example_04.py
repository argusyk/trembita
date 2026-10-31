# Розділ 23. Промислова експлуатація на Gemini Enterprise Agent Platform – приклад 4 (рукопис: 23-produkshn.md, рядок 256)
import json, logging, time
from opentelemetry import trace
from google.genai import types
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION

tracer = trace.get_tracer("trembita")
log = logging.getLogger("trembita.llm")


def generate_traced(client, contents, *, request_id: str, model: str = MODEL_MAIN):
    with tracer.start_as_current_span(f"chat {model}") as span:
        span.set_attribute("gen_ai.operation.name", "chat")
        span.set_attribute("gen_ai.request.model", model)
        t0 = time.perf_counter()
        resp = client.models.generate_content(
            model=model, contents=contents,
            config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION))
        u = resp.usage_metadata
        span.set_attribute("gen_ai.response.model", resp.model_version or model)
        span.set_attribute("gen_ai.usage.input_tokens", u.prompt_token_count or 0)
        span.set_attribute("gen_ai.usage.output_tokens", u.candidates_token_count or 0)
        log.info(json.dumps({
            "request_id": request_id, "model": resp.model_version,
            "latency_ms": round((time.perf_counter() - t0) * 1000),
            "finish_reason": str(resp.candidates[0].finish_reason),
            "tokens_in": u.prompt_token_count, "tokens_out": u.candidates_token_count,
            "tokens_thoughts": u.thoughts_token_count,     # тарифікуються як вихідні
            "tokens_cached": u.cached_content_token_count,
            "traffic_type": str(u.traffic_type),
        }, ensure_ascii=False))
        return resp
