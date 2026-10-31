"""«Трембіта» як команда агентів на ADK (розділ 15). Потребує google-adk.

Диспетчер працює на MODEL_MAIN (обробляє кожну репліку – каскад розділу 13), Argon – лише
в укладача й рецензента конвеєра претензій. На безкоштовному рівні задайте
TREMBITA_MODEL_SMART=gemini-3.8-flash.
"""
from google.adk.agents import Agent
from google.adk.tools import AgentTool

from trembita.agents.claims import claim_pipeline, register_claim
from trembita.agents.customs import customs_agent
from trembita.agents.tracker import tracker_agent
from trembita.config import MODEL_LITE, MODEL_MAIN
from trembita.tools import get_tariff

tariff_agent = Agent(
    name="tariff", model=MODEL_LITE, tools=[get_tariff],
    description="Рахує вартість перевезення за маршрутом, вагою й об'ємом.",
    instruction="Порахуй тариф через get_tariff і поверни суму та умови одним абзацом.")

dispatcher = Agent(
    name="dispatcher",
    model=MODEL_MAIN,
    description="Диспетчер-координатор «Трембіти».",
    instruction=(
        "Ти приймаєш звернення клієнтів «Смереки». Питання про місце вантажу "
        "передавай tracker, митні питання – customs. Претензію спершу зафіксуй "
        "інструментом register_claim (текст претензії й дані CMR, якщо є), а тоді "
        "передай claim_pipeline. Вартість рахуй інструментом tariff сам і розмову "
        "при цьому не передавай."
    ),
    sub_agents=[tracker_agent, claim_pipeline, customs_agent],   # передавання керування
    tools=[AgentTool(agent=tariff_agent), register_claim],       # агент як інструмент + запис стану
)
root_agent = dispatcher
