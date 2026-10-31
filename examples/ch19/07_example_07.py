# Розділ 19. Безпека застосунків і ризики – приклад 7 (рукопис: 19-bezpeka-zastosunkiv.md, рядок 322)
from typing import Any, Optional
from google.adk.agents import Agent
from google.adk.tools import BaseTool, FunctionTool, ToolContext
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION
from trembita.tools import create_pickup, find_warehouse, track_shipment

MAX_PICKUP_KG = 1500.0

def policy_guard(tool: BaseTool, args: dict[str, Any],
                 tool_context: ToolContext) -> Optional[dict]:
    """Детерміновані правила поверх моделі: модель їх не обійде."""
    if tool.name == "create_pickup":
        if float(args.get("weight_kg", 0)) > MAX_PICKUP_KG:
            return {"error": "Понад 1500 кг: оформлення лише через диспетчера."}
        if tool_context.state.get("untrusted_content_seen"):
            return {"error": "Після читання зовнішніх документів дія недоступна."}
    return None                                    # None означає: виконати інструмент

dispatcher = Agent(
    name="trembita_dispatch",
    model=MODEL_MAIN,
    instruction=SYSTEM_INSTRUCTION,
    tools=[track_shipment, find_warehouse,
           FunctionTool(create_pickup, require_confirmation=True)],  # питає людину
    before_tool_callback=policy_guard,
)
