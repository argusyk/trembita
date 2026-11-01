# Chapter 18. Gemini for Knowledge Work: Workspace, NotebookLM, Deep Research and Gemini Enterprise – example 1 (manuscript: 18-znannieva-robota.md, line 114)
# A review of the freight market to the EU by the Deep Research agent in background mode
import time

from google import genai

client = genai.Client()
DR_AGENT = "deep-research-preview-04-2026"   # preview: check the current ID in the documentation

TOPIC = (
    "Review of the road freight market from Ukraine to EU countries for 2025–2026: "
    "volumes, the situation at border crossings with Poland, Slovakia, Hungary and Romania, "
    "the permit regime, electronic CMRs, the main market players. "
    "Add a source and a date to every number; mark conflicting data separately."
)


def wait(job, pause: int = 60):
    """Poll the state of a background interaction until it finishes."""
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
    print("Status:", job.status, job.errors)
