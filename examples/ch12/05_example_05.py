# Розділ 12. Заземлення та вбудовані інструменти – приклад 5 (рукопис: 12-zazemlennia.md, рядок 206)
from google import genai
from google.genai import types

client = genai.Client()

order = ("Клієнт: 14 коробок 60×40×45 см по 12 кг, 2 палети 120×80×160 см по 310 кг, "
         "1 рулон Ø50 см довжиною 2 м, 25 кг. Коефіцієнт: 1 м³ = 250 кг.")
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=order + " Порахуй кодом об'єм, фактичну, об'ємну й розрахункову вагу.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution())],
    ),
)
for part in resp.candidates[0].content.parts:
    if part.executable_code:
        print("КОД:\n", part.executable_code.code)
    elif part.code_execution_result:
        print("РЕЗУЛЬТАТ:", part.code_execution_result.outcome, part.code_execution_result.output)
    elif part.text:
        print(part.text)
