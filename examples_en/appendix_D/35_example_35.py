# Appendix D. Code Recipes – example 35 (manuscript: 93-appendix-d.md, line 710)
from google.adk.a2a.utils.agent_to_a2a import to_a2a
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH, RemoteA2aAgent

# 1) a separate read-only agent; run behind a proxy with authentication:
#    uvicorn server_tracker:app (uvicorn itself is not reachable from outside)
app = to_a2a(agent, host="agents.smereka.example", port=443, protocol="https")

# 2) the partner's agent as a sub-agent
dunai_cargo = RemoteA2aAgent(
    name="dunai_cargo",
    description="Agent of the carrier Dunai Cargo: trips to the EU, booking of space.",
    agent_card=f"https://agents.dunai-cargo.example{AGENT_CARD_WELL_KNOWN_PATH}")
customs_agent = Agent(name="customs", model="gemini-3.8-flash",
                      instruction="Ask dunai_cargo about trips and space.",
                      sub_agents=[dunai_cargo])
