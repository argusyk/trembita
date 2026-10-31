# Розділ 10. Виклик функцій – приклад 5 (рукопис: 10-funktsii.md, рядок 240)
from google.genai import types

force_tracking = types.ToolConfig(
    function_calling_config=types.FunctionCallingConfig(
        mode=types.FunctionCallingConfigMode.ANY,
        allowed_function_names=["track_shipment"],   # модель мусить викликати лише цю
    )
)
config = types.GenerateContentConfig(
    tools=[smereka_tools],
    tool_config=force_tracking,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)
