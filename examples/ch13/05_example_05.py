# Розділ 13. Оптимізація: кешування контексту, пакетна обробка й вартість – приклад 5 (рукопис: 13-optymizatsiya.md, рядок 257)
from google import genai
from google.genai import types
from trembita.config import MODEL_LITE

client = genai.Client()
reviews = ["Вантаж прибув на день раніше, дякую!", "Третій день не можу додзвонитися."]
requests = [
    types.InlinedRequest(
        contents="Тональність відгуку одним словом (позитивна/нейтральна/негативна):\n" + text,
        metadata={"review_id": str(i)},
    )
    for i, text in enumerate(reviews)
]
job = client.batches.create(
    model=MODEL_LITE,
    src=requests,
    config=types.CreateBatchJobConfig(display_name="vidguky-2026-10-30"),
)
print(job.name, job.state)
