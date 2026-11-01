# Chapter 10. Function Calling – example 5 (manuscript: 10-funktsii.md, line 250)
from google.genai import types

force_tracking = types.ToolConfig(
    function_calling_config=types.FunctionCallingConfig(
        mode=types.FunctionCallingConfigMode.ANY,
        allowed_function_names=["track_shipment"],   # the model must call only this one
    )
)
config = types.GenerateContentConfig(
    tools=[smereka_tools],
    tool_config=force_tracking,
    automatic_function_calling=types.AutomaticFunctionCallingConfig(disable=True),
)
