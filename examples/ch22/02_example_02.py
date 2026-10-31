# Розділ 22. Комп'ютерне використання та браузерні агенти – приклад 2 (рукопис: 22-computer-use.md, рядок 93)
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_MAIN

client = make_client()
MODEL_CU = MODEL_MAIN     # gemini-3.8-flash; звірте з документацією, які моделі мають computer_use

# Дії, яких не вміє наш виконавець (підрозділ 22.4); назви обох поколінь – за кодом ADK 2.13
UNSUPPORTED = ["drag_and_drop", "search", "go_forward", "open_web_browser", "triple_click",
               "middle_click", "mouse_down", "mouse_up", "key_down", "key_up"]

cu_tool = types.Tool(computer_use=types.ComputerUse(
    environment=types.Environment.ENVIRONMENT_BROWSER,
    excluded_predefined_functions=UNSUPPORTED,          # звужуємо простір дій
))
config = types.GenerateContentConfig(
    tools=[cu_tool],
    thinking_config=types.ThinkingConfig(thinking_level="medium"),
)

contents = [types.Content(role="user", parts=[
    types.Part(text="Відкрий форму нової декларації й заповни розділ «Відправник»."),
    types.Part.from_bytes(data=page.screenshot(type="png"), mime_type="image/png"),
])]
resp = client.models.generate_content(model=MODEL_CU, contents=contents, config=config)
for call in resp.function_calls or []:
    print(call.name, call.args)          # напр. click {'x': 412, 'y': 233}
