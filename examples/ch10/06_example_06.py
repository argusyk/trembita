# Розділ 10. Виклик функцій – приклад 6 (рукопис: 10-funktsii.md, рядок 278)
from concurrent.futures import ThreadPoolExecutor
from google.genai import types

def execute_calls(function_calls, registry) -> types.Content:
    """Виконує паралельні виклики одночасно й повертає одну репліку з усіма результатами."""
    def run(fc):
        try:
            return registry[fc.name](**(fc.args or {}))
        except Exception as exc:
            return {"error": str(exc)}
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(run, function_calls))       # порядок збережено
    return types.Content(role="user", parts=[
        types.Part(function_response=types.FunctionResponse(id=fc.id, name=fc.name, response=r))
        for fc, r in zip(function_calls, results)])
