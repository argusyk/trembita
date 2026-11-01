# Appendix D. Code Recipes – example 26 (manuscript: 93-appendix-d.md, line 500)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="14 boxes of 60×40×45 cm, 12 kg each; 1 m³ = 250 kg. Use code to compute the chargeable weight.",
    config=types.GenerateContentConfig(tools=[types.Tool(code_execution=types.ToolCodeExecution())]),
)
content = resp.candidates[0].content if resp.candidates else None
for part in (content.parts or []) if content else []:
    if part.executable_code:
        print("CODE:\n", part.executable_code.code)
    elif part.code_execution_result:
        print("RESULT:", part.code_execution_result.output)
