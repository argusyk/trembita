# Додаток А. Практикум – приклад 9 (рукопис: 90-dodatok-a.md, рядок 418)
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from trembita.config import MODEL_MAIN
from trembita.tools import create_pickup, find_warehouse, track_shipment  # замініть своїми

root_agent = Agent(
    name="booking",
    model=MODEL_MAIN,
    description="Перевіряє наявність і оформлює бронювання для клієнтів.",
    instruction="Перш ніж бронювати, перевір наявність. Дані бери лише з інструментів.",
    tools=[track_shipment, find_warehouse,
           FunctionTool(create_pickup, require_confirmation=True)],   # дія після згоди людини
    output_key="booking_summary",
)
