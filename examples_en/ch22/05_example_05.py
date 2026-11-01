# Chapter 22. Computer Use and Browser Agents – example 5 (manuscript: 22-computer-use.md, line 238)
def run_task(page: Page, task: str, max_steps: int = 40) -> str:
    shot = page.screenshot(type="png")
    contents = [types.Content(role="user", parts=[
        types.Part(text=task), types.Part.from_bytes(data=shot, mime_type="image/png")])]
    for step in range(max_steps):
        resp = client.models.generate_content(model=MODEL_CU, contents=contents, config=config)
        if not resp.candidates:
            return "The model returned no response (the request may have been blocked)"
        contents.append(resp.candidates[0].content)       # together with thought signatures
        if not resp.function_calls:
            return resp.text or ""                        # the model has finished the task
        replies = []
        for call in resp.function_calls:
            if call.name == "broker_review":              # custom function (Section 22.8)
                return (call.args or {}).get("summary", "")   # no browser action at all
            args, extra = dict(call.args or {}), {}
            decision = args.pop("safety_decision", None)
            if decision and decision.get("decision") == "require_confirmation":
                if not ask_human(call.name, args, decision.get("explanation", "")):
                    return f"Stopped by a human at step {step}: {call.name}"
                extra["safety_acknowledgement"] = "true"
            execute(page, call.name, args)
            replies.append(types.Part.from_function_response(
                name=call.name,
                response={"url": page.url, **extra},
                parts=[types.FunctionResponsePart(inline_data=types.FunctionResponseBlob(
                    mime_type="image/png", data=page.screenshot(type="png")))],
            ))
        contents.append(types.Content(role="user", parts=replies))
    return "Step limit exceeded"
