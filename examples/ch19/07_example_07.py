# Розділ 19. Безпека застосунків і ризики – приклад 7 (рукопис: 19-bezpeka-zastosunkiv.md, рядок 361)
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION
from trembita.security import flag_untrusted, policy_guard
from trembita.tools import create_pickup, find_warehouse, track_shipment

def read_email(message_id: str) -> dict:
    """Повертає тему й текст листа клієнта зі скриньки відділу претензій."""
    ...  # інтеграція з поштою «Смереки» – поза пакетом trembita

dispatcher = Agent(
    name="trembita_dispatch",
    model=MODEL_MAIN,
    instruction=SYSTEM_INSTRUCTION,
    tools=[track_shipment, find_warehouse, read_email,
           FunctionTool(create_pickup, require_confirmation=True)],  # питає людину
    before_tool_callback=policy_guard,      # правила до виконання інструмента
    after_tool_callback=flag_untrusted,     # прапорець після read_email
)
