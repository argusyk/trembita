# Chapter 15. Agents on Gemini: the Agent Development Kit and the A2A protocol – example 5 (manuscript: 15-ahenty-adk.md, line 312)
from typing import Any, Optional

from google.adk.agents import Agent, RunConfig
from google.adk.tools import BaseTool, FunctionTool, ToolContext

from trembita.config import MODEL_MAIN
from trembita.pickup_guard import MAX_PICKUP_KG     # 24,000 kg: one limit for the whole book
from trembita.tools import create_pickup, track_shipment


def guard_pickup(tool: BaseTool, args: dict[str, Any], tool_context: ToolContext) -> Optional[dict]:
    """before_tool: a hard rule that does not depend on the model."""
    if tool.name != "create_pickup":
        return None
    try:
        weight = float(args.get("weight_kg", 0))
    except (TypeError, ValueError):
        return {"status": "rejected", "reason": "weight must be a number"}
    if weight > MAX_PICKUP_KG:
        return {"status": "rejected", "reason": f"over {MAX_PICKUP_KG} kg: only through a dispatcher"}
    return None                                    # None -> the tool is executed


def audit_tool(tool: BaseTool, args: dict[str, Any], tool_context: ToolContext,
               tool_response: dict) -> Optional[dict]:
    tool_context.state["temp:last_tool"] = tool.name
    print(f"[audit] {tool.name} {args} -> {tool_response.get('status')}")
    return None                                    # we do not replace the result


pickup_agent = Agent(
    name="pickup", model=MODEL_MAIN,
    instruction="Arrange cargo pickups. Before create_pickup, repeat the address, date and weight.",
    tools=[track_shipment, FunctionTool(create_pickup, require_confirmation=True)],
    before_tool_callback=guard_pickup,
    after_tool_callback=audit_tool,
)
run_config = RunConfig(max_llm_calls=25)           # safeguard against looping
