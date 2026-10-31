# Розділ 22. Комп'ютерне використання та браузерні агенти – приклад 2 (рукопис: 22-computer-use.md, рядок 93)
from google import genai
from google.genai import types

client = genai.Client()
MODEL_CU = "gemini-3.8-flash"     # звірте з документацією, які моделі мають computer_use

cu_tool = types.Tool(computer_use=types.ComputerUse(
    environment=types.Environment.ENVIRONMENT_BROWSER,
    excluded_predefined_functions=["drag_and_drop"],   # звужуємо простір дій
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
