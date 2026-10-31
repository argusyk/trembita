# Розділ 23. Промислова експлуатація на Gemini Enterprise Agent Platform – приклад 7 (рукопис: 23-produkshn.md, рядок 327)
def generate_traced(client, contents, *, request_id: str, model: str = MODEL_MAIN):
    with tracer.start_as_current_span(f"chat {model}") as span:
        span.set_attribute("gen_ai.operation.name", "chat")
        span.set_attribute("gen_ai.request.model", model)
        t0, rec = time.perf_counter(), {"request_id": request_id, "model": model}
        try:
            resp = client.models.generate_content(
                model=model, contents=contents,
                config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION))
        except Exception as e:                        # невдалий виклик теж іде в журнал
            span.record_exception(e)
            span.set_status(Status(StatusCode.ERROR, type(e).__name__))
            rec.update(status="error", error=type(e).__name__, code=getattr(e, "code", None),
                       latency_ms=round((time.perf_counter() - t0) * 1000))
            log.error(json.dumps(rec, ensure_ascii=False))
            raise
        rec.update(status="ok", latency_ms=round((time.perf_counter() - t0) * 1000),
                   **usage_record(resp))
        span.set_attribute("gen_ai.response.model", resp.model_version or model)
        span.set_attribute("gen_ai.usage.input_tokens", rec["tokens_in"] or 0)
        span.set_attribute("gen_ai.usage.output_tokens", rec["tokens_out"] or 0)
        log.info(json.dumps(rec, ensure_ascii=False))
        return resp
