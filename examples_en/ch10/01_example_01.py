# Chapter 10. Function Calling – example 1 (manuscript: 10-funktsii.md, line 50)
from google.genai import types

get_tariff_decl = types.FunctionDeclaration(
    name="get_tariff",
    description="Calculates the cost of transporting cargo by Smereka between two "
                "cities. Call it when the customer asks about the delivery price or compares options.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "origin": {"type": "string", "description": "City of origin, e.g. 'Lviv'"},
            "destination": {"type": "string", "description": "City of destination"},
            "weight_kg": {"type": "number", "exclusiveMinimum": 0, "maximum": 24000},
            "volume_m3": {"type": "number", "minimum": 0, "default": 0.0},
        },
        "required": ["origin", "destination", "weight_kg"],
    },
)

track_decl = types.FunctionDeclaration(
    name="track_shipment",
    description="Returns the current status and location of a shipment. Call it "
                "when the request contains a shipment number like SM-2610-0042.",
    parameters_json_schema={
        "type": "object",
        "properties": {"shipment_id": {"type": "string", "pattern": "^SM-\\d{4}-\\d{4}$"}},
        "required": ["shipment_id"],
    },
)

smereka_tools = types.Tool(function_declarations=[get_tariff_decl, track_decl])
