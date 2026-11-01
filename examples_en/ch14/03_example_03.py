# Chapter 14. The Live API and media generation – example 3 (manuscript: 14-live-media.md, line 151)
import asyncio
from google.genai import types
from trembita.tools import create_pickup, find_warehouse, track_shipment

TOOLS = {"track_shipment": track_shipment, "find_warehouse": find_warehouse,
         "create_pickup": create_pickup}      # only queues the request in PickupGuard


async def run_tool(fc: types.FunctionCall, show_confirm_button) -> dict:
    fn = TOOLS.get(fc.name)
    if fn is None:
        return {"error": f"unknown function {fc.name}"}
    try:   # a synchronous function runs in a separate thread so the event loop keeps playing sound
        result = await asyncio.to_thread(fn, **(fc.args or {}))
    except Exception as e:
        return {"error": f"{type(e).__name__}: {e}"}
    if fc.name == "create_pickup" and result.get("status") == "awaiting_human_confirmation":
        show_confirm_button(result.pop("token"), fc.args)   # the button will call guard.confirm
        result["message"] = "The request has been prepared; the driver confirms it with a button in the app."
    return result


async def handle_tool_call(session, msg: types.LiveServerMessage, show_confirm_button) -> None:
    calls = msg.tool_call.function_calls or []
    results = await asyncio.gather(*(run_tool(fc, show_confirm_button) for fc in calls))
    await session.send_tool_response(function_responses=[
        types.FunctionResponse(id=fc.id, name=fc.name, response=r) for fc, r in zip(calls, results)])
