# Appendix D. Code Recipes – example 13 (manuscript: 93-appendix-d.md, line 225)
get_tariff_decl = types.FunctionDeclaration(
    name="get_tariff",
    description="Cost of transport between cities. Call it when asked about the price of delivery.",
    parameters_json_schema={
        "type": "object",
        "properties": {
            "origin": {"type": "string"},
            "destination": {"type": "string"},
            "weight_kg": {"type": "number", "exclusiveMinimum": 0, "maximum": 24000},
        },
        "required": ["origin", "destination", "weight_kg"],
    },
)
smereka_tools = types.Tool(function_declarations=[get_tariff_decl])
