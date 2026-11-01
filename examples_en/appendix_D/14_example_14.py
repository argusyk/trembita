# Appendix D. Code Recipes – example 14 (manuscript: 93-appendix-d.md, line 246)
REGISTRY = {"get_tariff": get_tariff}
cfg = types.GenerateContentConfig(
    tools=[smereka_tools],
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True))

def run_with_tools(question: str, max_steps: int = 6) -> str:
    history = [types.Content(role="user", parts=[types.Part(text=question)])]
    for _ in range(max_steps):
        resp = client.models.generate_content(model="gemini-3.8-flash", contents=history, config=cfg)
        if not resp.function_calls:
            return resp.text or ""
        history.append(resp.candidates[0].content)     # calls together with thought signatures
        parts = []
        for fc in resp.function_calls:
            try:
                result = REGISTRY[fc.name](**fc.args)
            except Exception as exc:                   # the error goes back to the model as data
                result = {"error": str(exc)}
            parts.append(types.Part(function_response=types.FunctionResponse(
                id=fc.id, name=fc.name, response=result)))
        history.append(types.Content(role="user", parts=parts))
    return "Could not answer within the allotted number of steps."
