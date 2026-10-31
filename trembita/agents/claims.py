"""Конвеєр розбору претензій: паралельний збір фактів і цикл «чернетка – рецензія» (розділ 15)."""
from google.adk.agents import Agent, LoopAgent, ParallelAgent, SequentialAgent
from google.adk.tools import exit_loop

from trembita.config import MODEL_MAIN, MODEL_SMART
from trembita.tools import track_shipment

route_facts = Agent(
    name="route_facts", model=MODEL_MAIN, tools=[track_shipment],
    instruction="Віднови історію руху відправлення з претензії:\n{claim_text}",
    output_key="route_facts")
doc_facts = Agent(
    name="doc_facts", model=MODEL_MAIN,
    instruction="Випиши з CMR вантаж, вагу й застереження перевізника:\n{cmr_text}",
    output_key="doc_facts")
drafter = Agent(
    name="drafter", model=MODEL_SMART,
    instruction=("Склади проєкт відповіді на претензію.\nРух вантажу: {route_facts}\n"
                 "Документи: {doc_facts}\nЗауваги рецензента: {review?}"),
    output_key="draft")
reviewer = Agent(
    name="reviewer", model=MODEL_SMART, tools=[exit_loop],
    instruction=("Перевір проєкт: {draft}\nЯкщо кожне твердження спирається на факти "
                 "і немає визнання провини без підстав, виклич exit_loop. "
                 "Інакше коротко перелічи зауваги."),
    output_key="review")

claim_pipeline = SequentialAgent(
    name="claim_pipeline",
    description="Розбирає претензію клієнта й готує проєкт відповіді для юриста.",
    sub_agents=[
        ParallelAgent(name="gather_facts", sub_agents=[route_facts, doc_facts]),
        LoopAgent(name="draft_review", sub_agents=[drafter, reviewer], max_iterations=3),
    ],
)
