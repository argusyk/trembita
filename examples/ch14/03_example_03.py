# Розділ 14. Live API і генерація медіа – приклад 3 (рукопис: 14-live-media.md, рядок 151)
import asyncio
from google.genai import types
from trembita.tools import create_pickup, find_warehouse, track_shipment

TOOLS = {"track_shipment": track_shipment, "find_warehouse": find_warehouse,
         "create_pickup": create_pickup}      # лише ставить заявку в чергу PickupGuard


async def run_tool(fc: types.FunctionCall, show_confirm_button) -> dict:
    fn = TOOLS.get(fc.name)
    if fn is None:
        return {"error": f"невідома функція {fc.name}"}
    try:   # синхронна функція – в окремому потоці, щоб цикл подій далі відтворював звук
        result = await asyncio.to_thread(fn, **(fc.args or {}))
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}
    if fc.name == "create_pickup" and result.get("status") == "awaiting_human_confirmation":
        show_confirm_button(result.pop("token"), fc.args)   # кнопка викличе guard.confirm
        result["message"] = "Заявку підготовлено; водій підтверджує її кнопкою в застосунку."
    return result


async def handle_tool_call(session, msg: types.LiveServerMessage, show_confirm_button) -> None:
    calls = msg.tool_call.function_calls or []
    results = await asyncio.gather(*(run_tool(fc, show_confirm_button) for fc in calls))
    await session.send_tool_response(function_responses=[
        types.FunctionResponse(id=fc.id, name=fc.name, response=r) for fc, r in zip(calls, results)])
