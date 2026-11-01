# Chapter 19. Application Security and Risks – example 7 (manuscript: 19-bezpeka-zastosunkiv.md, line 361)
from google.adk.agents import Agent
from google.adk.tools import FunctionTool
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION
from trembita.security import flag_untrusted, policy_guard
from trembita.tools import create_pickup, find_warehouse, track_shipment

def read_email(message_id: str) -> dict:
    """Returns the subject and text of a customer's email from the claims department mailbox."""
    ...  # integration with Smereka's mail is outside the trembita package

dispatcher = Agent(
    name="trembita_dispatch",
    model=MODEL_MAIN,
    instruction=SYSTEM_INSTRUCTION,
    tools=[track_shipment, find_warehouse, read_email,
           FunctionTool(create_pickup, require_confirmation=True)],  # asks a human
    before_tool_callback=policy_guard,      # rules before the tool runs
    after_tool_callback=flag_untrusted,     # flag after read_email
)
