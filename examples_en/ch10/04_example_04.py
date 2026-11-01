# Chapter 10. Function Calling – example 4 (manuscript: 10-funktsii.md, line 188)
from google import genai
from google.genai import types
from trembita.config import MODEL_MAIN
from trembita.tools import track_shipment, get_tariff, find_warehouse

client = genai.Client()
resp = client.models.generate_content(
    model=MODEL_MAIN,
    contents="Where is SM-2610-0042 now? And how much will another 800 kg from Lviv to Uzhhorod cost?",
    config=types.GenerateContentConfig(
        tools=[track_shipment, get_tariff, find_warehouse],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(maximum_remote_calls=5),
    ),
)
print(resp.text)
for step in resp.automatic_function_calling_history or []:
    for part in step.parts:
        if part.function_call:
            print("call:", part.function_call.name, dict(part.function_call.args))
