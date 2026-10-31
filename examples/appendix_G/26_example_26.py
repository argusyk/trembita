# Додаток Г. Довідник рецептів коду – приклад 26 (рукопис: 93-dodatok-g.md, рядок 500)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="14 коробок 60×40×45 см по 12 кг; 1 м³ = 250 кг. Порахуй кодом розрахункову вагу.",
    config=types.GenerateContentConfig(tools=[types.Tool(code_execution=types.ToolCodeExecution())]),
)
content = resp.candidates[0].content if resp.candidates else None
for part in (content.parts or []) if content else []:
    if part.executable_code:
        print("КОД:\n", part.executable_code.code)
    elif part.code_execution_result:
        print("РЕЗУЛЬТАТ:", part.code_execution_result.output)
