"""Агент відстеження (розділ 15)."""
from google.adk.agents import Agent
from google.adk.tools import ToolContext
from google.genai import types

from trembita.config import MODEL_MAIN
from trembita.tools import find_warehouse, track_shipment


def remember_client(name: str, tool_context: ToolContext) -> dict:
    """Запам'ятовує назву компанії-клієнта для наступних розмов."""
    tool_context.state["user:client_name"] = name   # зміна потрапить у подію
    return {"status": "ok"}


tracker_agent = Agent(
    name="tracker",
    model=MODEL_MAIN,
    description="Відстежує відправлення «Смереки» за номером і знаходить склади.",
    instruction=(
        "Ти – агент відстеження компанії «Смерека». Клієнт: {user:client_name?}.\n"
        "Номер відправлення має вигляд SM-2610-0042; якщо його немає, попроси.\n"
        "Статус бери лише з track_shipment і нічого не домислюй."
    ),
    tools=[track_shipment, find_warehouse, remember_client],
    output_key="tracking_summary",          # фінальна відповідь -> session.state
    generate_content_config=types.GenerateContentConfig(
        max_output_tokens=1024,
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
)
