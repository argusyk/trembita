# Розділ 15. Агенти на Gemini: Agent Development Kit і протокол A2A – приклад 6 (рукопис: 15-ahenty-adk.md, рядок 382)
# 1) «Смерека» відкриває окремий екземпляр трекера партнерам: server_tracker.py
from google.adk.a2a.utils.agent_to_a2a import to_a2a

from trembita.agents.tracker import tracker_agent

app = to_a2a(tracker_agent, host="agents.smereka.example", port=443, protocol="https")
# запуск: uvicorn server_tracker:app --host 0.0.0.0 --port 8001 (за зворотним проксі)

# 2) «Смерека» підключає агента партнера: trembita/agents/customs.py
from google.adk.agents import Agent
from google.adk.agents.remote_a2a_agent import AGENT_CARD_WELL_KNOWN_PATH, RemoteA2aAgent

from trembita.config import MODEL_MAIN

dunai_cargo = RemoteA2aAgent(
    name="dunai_cargo",
    description="Агент перевізника «Дунай-Карго»: рейси до ЄС, бронювання місць.",
    agent_card=f"https://agents.dunai-cargo.example{AGENT_CARD_WELL_KNOWN_PATH}",
)
customs_agent = Agent(
    name="customs", model=MODEL_MAIN,
    description="Митне оформлення експорту до ЄС і стикування з рейсами партнера.",
    instruction="Перевір готовність документів; про рейси й місця питай dunai_cargo.",
    sub_agents=[dunai_cargo],
)
