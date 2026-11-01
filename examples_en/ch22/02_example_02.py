# Chapter 22. Computer Use and Browser Agents – example 2 (manuscript: 22-computer-use.md, line 93)
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_MAIN

client = make_client()
MODEL_CU = MODEL_MAIN     # gemini-3.8-flash; check the docs for which models have computer_use

# Actions our executor cannot perform (Section 22.4); names of both generations as in ADK 2.13 code
UNSUPPORTED = ["drag_and_drop", "search", "go_forward", "open_web_browser", "triple_click",
               "middle_click", "mouse_down", "mouse_up", "key_down", "key_up"]

cu_tool = types.Tool(computer_use=types.ComputerUse(
    environment=types.Environment.ENVIRONMENT_BROWSER,
    excluded_predefined_functions=UNSUPPORTED,          # narrow the action space
))
config = types.GenerateContentConfig(
    tools=[cu_tool],
    thinking_config=types.ThinkingConfig(thinking_level="medium"),
)

contents = [types.Content(role="user", parts=[
    types.Part(text="Open the new declaration form and fill in the “Sender” section."),
    types.Part.from_bytes(data=page.screenshot(type="png"), mime_type="image/png"),
])]
resp = client.models.generate_content(model=MODEL_CU, contents=contents, config=config)
for call in resp.function_calls or []:
    print(call.name, call.args)          # e.g. click {'x': 412, 'y': 233}
