# Розділ 15. Агенти на Gemini: Agent Development Kit і протокол A2A – приклад 5 (рукопис: 15-ahenty-adk.md, рядок 289)
from typing import Any, Optional

from google.adk.agents import Agent, RunConfig
from google.adk.tools import BaseTool, FunctionTool, ToolContext

from trembita.config import MODEL_MAIN
from trembita.tools import create_pickup, track_shipment

MAX_PICKUP_KG = 20_000


def guard_pickup(tool: BaseTool, args: dict[str, Any], tool_context: ToolContext) -> Optional[dict]:
    """before_tool: жорстке правило, що не залежить від моделі."""
    if tool.name == "create_pickup" and float(args.get("weight_kg", 0)) > MAX_PICKUP_KG:
        return {"status": "rejected", "reason": "понад 20 т – лише через диспетчера"}
    return None                                    # None -> інструмент виконується


def audit_tool(tool: BaseTool, args: dict[str, Any], tool_context: ToolContext,
               tool_response: dict) -> Optional[dict]:
    tool_context.state["temp:last_tool"] = tool.name
    print(f"[аудит] {tool.name} {args} -> {tool_response.get('status')}")
    return None                                    # результат не підміняємо


pickup_agent = Agent(
    name="pickup", model=MODEL_MAIN,
    instruction="Оформлюй забір вантажу. Перед create_pickup повтори адресу, дату й вагу.",
    tools=[track_shipment, FunctionTool(create_pickup, require_confirmation=True)],
    before_tool_callback=guard_pickup,
    after_tool_callback=audit_tool,
)
run_config = RunConfig(max_llm_calls=25)           # запобіжник від зациклення
