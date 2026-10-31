# Розділ 17. Агентна розробка: Antigravity, Jules і Gemini Code Assist – приклад 2 (рукопис: 17-ahentna-rozrobka.md, рядок 224)
# Навчальний приклад: агент Antigravity виконує задачу у віддаленому середовищі
import time

from google import genai

client = genai.Client()

job = client.interactions.create(
    agent="antigravity-preview-05-2026",       # прев'ю: ID може змінитися
    input=("Допиши модульні тести для trembita/tools.py (get_tariff, find_warehouse), "
           "запусти pytest і коротко опиши результат. Код поза tests/ не змінюй."),
    environment={
        "type": "remote",
        "sources": [{"type": "repository",
                     "source": "github.com/smereka/trembita",     # умовний репозиторій
                     "target": "/workspace/trembita"}],
        # вихід у мережу лише до індексу пакетів
        "network": {"allowlist": [{"domain": "pypi.org"},
                                  {"domain": "files.pythonhosted.org"}]},
    },
    agent_config={"type": "antigravity", "max_total_tokens": 2_000_000},
    background=True,                            # фонове виконання
)
while job.status in ("queued", "in_progress"):
    time.sleep(30)
    job = client.interactions.get(job.id)
print(job.status)        # completed, failed, budget_exceeded ...
print(job.output_text)
