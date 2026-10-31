"""«Трембіта» як команда агентів на ADK (розділ 15). Потребує google-adk."""
from google.adk.agents import Agent
from google.adk.tools import AgentTool

from trembita.agents.claims import claim_pipeline
from trembita.agents.customs import customs_agent
from trembita.agents.tracker import tracker_agent
from trembita.config import MODEL_LITE, MODEL_SMART
from trembita.tools import get_tariff

tariff_agent = Agent(
    name="tariff", model=MODEL_LITE, tools=[get_tariff],
    description="Рахує вартість перевезення за маршрутом, вагою й об'ємом.",
    instruction="Порахуй тариф через get_tariff і поверни суму та умови одним абзацом.")

dispatcher = Agent(
    name="dispatcher",
    model=MODEL_SMART,
    description="Диспетчер-координатор «Трембіти».",
    instruction=(
        "Ти приймаєш звернення клієнтів «Смереки». Питання про місце вантажу "
        "передавай tracker, претензії – claim_pipeline, митні питання – customs. "
        "Вартість рахуй інструментом tariff сам і розмову при цьому не передавай."
    ),
    sub_agents=[tracker_agent, claim_pipeline, customs_agent],  # передавання керування
    tools=[AgentTool(agent=tariff_agent)],                      # агент як інструмент
)
root_agent = dispatcher
