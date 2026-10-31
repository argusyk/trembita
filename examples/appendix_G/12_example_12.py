# Додаток Г. Довідник рецептів коду – приклад 12 (рукопис: 93-dodatok-g.md, рядок 201)
def track_shipment(shipment_id: str) -> dict:
    """Статус відправлення за номером виду SM-2610-0042."""
    return {"status": "на митному контролі", "location": "Чоп"}

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Де зараз SM-2610-0042?",
    config=types.GenerateContentConfig(
        tools=[track_shipment],
        automatic_function_calling=types.AutomaticFunctionCallingConfig(maximum_remote_calls=5)),
)
print(resp.text)
for step in resp.automatic_function_calling_history or []:
    for part in step.parts:
        if part.function_call:
            print("виклик:", part.function_call.name, dict(part.function_call.args))
