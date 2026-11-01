# Chapter 12. Grounding and Built-in Tools – example 5 (manuscript: 12-zazemlennia.md, line 206)
from google import genai
from google.genai import types

client = genai.Client()

order = ("Customer: 14 boxes 60×40×45 cm, 12 kg each; 2 pallets 120×80×160 cm, 310 kg each; "
         "1 roll Ø50 cm, 2 m long, 25 kg. Factor: 1 m³ = 250 kg.")
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=order + " Use code to calculate the volume and the actual, volumetric and chargeable weight.",
    config=types.GenerateContentConfig(
        tools=[types.Tool(code_execution=types.ToolCodeExecution())],
    ),
)
for part in resp.candidates[0].content.parts:
    if part.executable_code:
        print("CODE:\n", part.executable_code.code)
    elif part.code_execution_result:
        print("RESULT:", part.code_execution_result.outcome, part.code_execution_result.output)
    elif part.text:
        print(part.text)
