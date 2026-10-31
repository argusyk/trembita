# Додаток Г. Довідник рецептів коду – приклад 13 (рукопис: 93-dodatok-g.md, рядок 224)
get_tariff_decl = types.FunctionDeclaration(
    name="get_tariff",
    description="Вартість перевезення між містами. Викликай, коли питають ціну доставки.",
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
