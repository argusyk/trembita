# Розділ 14. Live API і генерація медіа – приклад 3 (рукопис: 14-live-media.md, рядок 151)
from google.genai import types
from trembita.tools import find_warehouse, track_shipment

TOOLS = {"track_shipment": track_shipment, "find_warehouse": find_warehouse}


async def handle_tool_call(session, msg: types.LiveServerMessage) -> None:
    responses = []
    for fc in msg.tool_call.function_calls:
        fn = TOOLS.get(fc.name)
        result = fn(**fc.args) if fn else {"error": f"невідома функція {fc.name}"}
        responses.append(types.FunctionResponse(id=fc.id, name=fc.name, response=result))
    await session.send_tool_response(function_responses=responses)
