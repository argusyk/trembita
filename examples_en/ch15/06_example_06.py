# Chapter 15. Agents on Gemini: the Agent Development Kit and the A2A protocol – example 6 (manuscript: 15-ahenty-adk.md, line 410)
# 1) Smereka exposes a separate read-only tracker to partners: server_tracker.py
from trembita.agents.tracker import make_partner_a2a_app

app = make_partner_a2a_app()   # inside: to_a2a(partner_tracker_agent, host=..., port=443, protocol="https")
# run: uvicorn server_tracker:app --host 0.0.0.0 --port 8001 (behind a proxy with authentication)

# 2) Smereka connects the partner's agent: trembita/agents/customs.py
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH, RemoteA2aAgent

from trembita.config import MODEL_MAIN

dunai_cargo = RemoteA2aAgent(
    name="dunai_cargo",
    description="Agent of the carrier Dunai Cargo: runs to the EU, space booking.",
    agent_card=f"https://agents.dunai-cargo.example{AGENT_CARD_WELL_KNOWN_PATH}",
)
customs_agent = Agent(
    name="customs", model=MODEL_MAIN,
    description="Customs clearance of exports to the EU and connection with the partner's runs.",
    instruction="Check that the documents are ready; ask dunai_cargo about runs and space.",
    sub_agents=[dunai_cargo],
)
