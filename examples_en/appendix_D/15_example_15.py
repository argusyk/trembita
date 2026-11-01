# Appendix D. Code Recipes – example 15 (manuscript: 93-appendix-d.md, line 275)
config = types.GenerateContentConfig(
    tools=[smereka_tools],
    tool_config=types.ToolConfig(function_calling_config=types.FunctionCallingConfig(
        mode=types.FunctionCallingConfigMode.ANY,      # AUTO | ANY | NONE | VALIDATED
        allowed_function_names=["get_tariff"])),
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)
