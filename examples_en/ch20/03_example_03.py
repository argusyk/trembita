# Chapter 20. Evaluating Gemini Applications – example 3 (manuscript: 20-otsiniuvannia.md, line 184)
def judge(question: str, reference: str, answer: str, *, tool_outputs=None, model: str = MODEL_SMART,
          generator_models=(MODEL_MAIN,), client=None) -> Verdict | None:
    """Pointwise grade against the rubric. A judge of the same model as the generator is forbidden."""
    _check_judge(model, generator_models)        # ValueError if model is among generator_models
    resp = (client or make_client()).models.generate_content(
        model=model,
        contents="\n".join([_tag("question", question), _tag("reference", reference),
                            _tool_block(tool_outputs), _tag("answer", answer)]),
        config=types.GenerateContentConfig(
            system_instruction=RUBRIC, response_mime_type="application/json",
            response_schema=Verdict, thinking_config=types.ThinkingConfig(thinking_level="low")),
    )
    return resp.parsed if isinstance(resp.parsed, Verdict) else None
