# Розділ 22. Комп'ютерне використання та браузерні агенти – приклад 4 (рукопис: 22-computer-use.md, рядок 202)
def run_task(page: Page, task: str, max_steps: int = 40) -> str:
    shot = page.screenshot(type="png")
    contents = [types.Content(role="user", parts=[
        types.Part(text=task), types.Part.from_bytes(data=shot, mime_type="image/png")])]
    for step in range(max_steps):
        resp = client.models.generate_content(model=MODEL_CU, contents=contents, config=config)
        contents.append(resp.candidates[0].content)       # разом із підписами думок
        if not resp.function_calls:
            return resp.text or ""                        # модель завершила задачу
        replies = []
        for call in resp.function_calls:
            args, extra = dict(call.args or {}), {}
            decision = args.pop("safety_decision", None)
            if decision and decision.get("decision") == "require_confirmation":
                if not ask_human(call.name, args, decision.get("explanation", "")):
                    return f"Зупинено людиною на кроці {step}: {call.name}"
                extra["safety_acknowledgement"] = "true"
            execute(page, call.name, args)
            replies.append(types.Part.from_function_response(
                name=call.name,
                response={"url": page.url, **extra},
                parts=[types.FunctionResponsePart(inline_data=types.FunctionResponseBlob(
                    mime_type="image/png", data=page.screenshot(type="png")))],
            ))
        contents.append(types.Content(role="user", parts=replies))
    return "Перевищено ліміт кроків"
