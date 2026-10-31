# Розділ 10. Виклик функцій – приклад 1 (рукопис: 10-funktsii.md, рядок 50)
from google.genai import types

get_tariff_decl = types.FunctionDeclaration(
    name="get_tariff",
    description="Розраховує вартість перевезення вантажу компанією «Смерека» між двома "
                "містами. Викликай, коли клієнт питає ціну доставки або порівнює варіанти.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "origin": {"type": "string", "description": "Місто відправлення, напр. «Львів»"},
            "destination": {"type": "string", "description": "Місто призначення"},
            "weight_kg": {"type": "number", "exclusiveMinimum": 0, "maximum": 24000},
            "volume_m3": {"type": "number", "minimum": 0, "default": 0.0},
        },
        "required": ["origin", "destination", "weight_kg"],
    },
)

track_decl = types.FunctionDeclaration(
    name="track_shipment",
    description="Повертає поточний статус і місцезнаходження відправлення. Викликай, "
                "коли в запиті є номер відправлення виду SM-2610-0042.",
    parameters_json_schema={
        "type": "object",
        "properties": {"shipment_id": {"type": "string", "pattern": "^SM-\\d{4}-\\d{4}$"}},
        "required": ["shipment_id"],
    },
)

smereka_tools = types.Tool(function_declarations=[get_tariff_decl, track_decl])
