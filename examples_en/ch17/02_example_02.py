# Chapter 17. Agentic Development: Antigravity, Jules and Gemini Code Assist – example 2 (manuscript: 17-ahentna-rozrobka.md, line 230)
# Teaching example: the Antigravity agent carries out a task in a remote environment
import time

from google import genai

client = genai.Client()

job = client.interactions.create(
    agent="antigravity-preview-05-2026",       # preview: the ID may change
    input=("Write unit tests for trembita/tools.py (get_tariff, find_warehouse), "
           "run pytest and briefly describe the result. Do not change code outside tests/."),
    environment={
        "type": "remote",
        "sources": [{"type": "repository",
                     "source": "github.com/smereka/trembita",     # illustrative repository
                     "target": "/workspace/trembita"}],
        # network egress only to the package index
        "network": {"allowlist": [{"domain": "pypi.org"},
                                  {"domain": "files.pythonhosted.org"}]},
    },
    agent_config={"type": "antigravity", "max_total_tokens": 2_000_000},
    background=True,                            # background execution
)
while job.status in ("queued", "in_progress"):
    time.sleep(30)
    job = client.interactions.get(job.id)
print(job.status)        # completed, failed, budget_exceeded ...
print(job.output_text)
