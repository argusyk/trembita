"""Митний агент і віддалений агент партнера через A2A (розділ 15)."""
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
