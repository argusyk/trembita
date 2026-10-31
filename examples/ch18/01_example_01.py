# Розділ 18. Gemini для знаннєвої роботи: Workspace, NotebookLM, Deep Research і Gemini Enterprise – приклад 1 (рукопис: 18-znannieva-robota.md, рядок 112)
# Огляд ринку перевезень до ЄС агентом Deep Research у фоновому режимі
import time

from google import genai

client = genai.Client()
DR_AGENT = "deep-research-preview-04-2026"   # прев'ю: актуальний ID звіряйте з документацією

TOPIC = (
    "Огляд ринку автомобільних вантажних перевезень з України до країн ЄС за 2025–2026 роки: "
    "обсяги, ситуація на пунктах пропуску з Польщею, Словаччиною, Угорщиною й Румунією, "
    "дозвільний режим, електронні CMR, основні гравці ринку. "
    "До кожного числа додай джерело й дату; суперечливі дані познач окремо."
)


def wait(job, pause: int = 60):
    """Опитує стан фонової взаємодії, доки вона не завершиться."""
    while job.status in ("queued", "in_progress"):
        time.sleep(pause)
        job = client.interactions.get(job.id)
    return job


job = client.interactions.create(
    agent=DR_AGENT,
    input=TOPIC,
    agent_config={"type": "deep-research", "thinking_summaries": "auto"},
    background=True,
)
job = wait(job)
if job.status == "completed":
    with open("eu_market_review.md", "w", encoding="utf-8") as f:
        f.write(job.output_text or "")
else:
    print("Статус:", job.status, job.errors)
