# Appendix D. Code Recipes – example 12 (manuscript: 93-appendix-d.md, line 202)
def track_shipment(shipment_id: str) -> dict:
    """Status of a shipment by a number of the form SM-2610-0042."""
    return {"status": "under customs control", "location": "Chop"}

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Where is SM-2610-0042 now?",
    config=types.GenerateContentConfig(
        tools=[track_shipment],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(maximum_remote_calls=5)),
)
print(resp.text)
for step in resp.automatic_function_calling_history or []:
    for part in step.parts:
        if part.function_call:
            print("call:", part.function_call.name, dict(part.function_call.args))
