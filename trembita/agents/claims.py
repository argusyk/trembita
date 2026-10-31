"""Конвеєр розбору претензій: паралельний збір фактів і цикл «чернетка – рецензія» (розділ 15).

Вхідні дані конвеєр бере зі стану сесії: ключі claim_text і cmr_text записує інструмент
диспетчера register_claim перед передаванням керування. Підстановки {claim_text?} і {cmr_text?}
необов'язкові: якщо ключів немає, агент бере дані з історії розмови, а не падає з KeyError.
Argon (MODEL_SMART) працює лише в укладача й рецензента, збирачі фактів – на MODEL_MAIN.
"""
from google.adk.agents import Agent, LoopAgent, ParallelAgent, SequentialAgent
from google.adk.tools import ToolContext, exit_loop

from trembita.config import MODEL_MAIN, MODEL_SMART
from trembita.tools import track_shipment

CLAIM_KEYS = ("claim_text", "cmr_text")


def register_claim(claim_text: str, cmr_text: str, tool_context: ToolContext) -> dict:
    """Записує текст претензії й дані накладної CMR перед передаванням у claim_pipeline.

    Args:
        claim_text: текст претензії клієнта (дослівно, з номером відправлення).
        cmr_text: дані накладної CMR із розмови; порожній рядок, якщо клієнт їх не надав.
    """
    tool_context.state["claim_text"] = claim_text
    tool_context.state["cmr_text"] = cmr_text or "клієнт не надав даних накладної"
    return {"status": "ok"}


route_facts = Agent(
    name="route_facts", model=MODEL_MAIN, tools=[track_shipment],
    instruction=("Віднови історію руху відправлення з претензії. Якщо тексту нижче немає, "
                 "візьми претензію з розмови.\n{claim_text?}"),
    output_key="route_facts")
doc_facts = Agent(
    name="doc_facts", model=MODEL_MAIN,
    instruction=("Випиши з CMR вантаж, вагу й застереження перевізника. Якщо даних нижче "
                 "немає, візьми їх з розмови або напиши, що їх бракує.\n{cmr_text?}"),
    output_key="doc_facts")
drafter = Agent(
    name="drafter", model=MODEL_SMART,
    instruction=("Склади проєкт відповіді на претензію.\nРух вантажу: {route_facts}\n"
                 "Документи: {doc_facts}\nЗауваги рецензента: {review?}"),
    output_key="draft")
reviewer = Agent(
    name="reviewer", model=MODEL_SMART, tools=[exit_loop],
    instruction=("Перевір проєкт: {draft}\nФакти: {route_facts}\n{doc_facts}\n"
                 "Якщо кожне твердження спирається на факти і немає визнання провини без "
                 "підстав, виклич exit_loop. Інакше коротко перелічи зауваги."),
    output_key="review")

claim_pipeline = SequentialAgent(
    name="claim_pipeline",
    description="Розбирає претензію клієнта й готує проєкт відповіді для юриста.",
    sub_agents=[
        ParallelAgent(name="gather_facts", sub_agents=[route_facts, doc_facts]),
        LoopAgent(name="draft_review", sub_agents=[drafter, reviewer], max_iterations=3),
    ],
)
