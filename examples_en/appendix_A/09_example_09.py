# Appendix A. Laboratory Practicum – example 9 (manuscript: 90-appendix-a.md, line 442)
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from trembita.config import MODEL_MAIN
from trembita.tools import create_pickup, find_warehouse, track_shipment  # replace with your own

root_agent = Agent(
    name="booking",
    model=MODEL_MAIN,
    description="Checks availability and makes bookings for clients.",
    instruction="Check availability before booking. Take data only from the tools.",
    tools=[track_shipment, find_warehouse,
           FunctionTool(create_pickup, require_confirmation=True)],   # action after human consent
    output_key="booking_summary",
)
