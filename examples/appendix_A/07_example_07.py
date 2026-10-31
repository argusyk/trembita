# Додаток А. Практикум – приклад 7 (рукопис: 90-dodatok-a.md, рядок 335)
from google import genai
from google.genai import types
from trembita.config import MODEL_LITE

client = genai.Client()
MESSAGES = ["Не можу увійти в пошту з ранку", "Принтер на третьому поверсі не друкує"]
requests = [types.InlinedRequest(contents=f"Категорія звернення одним словом:\n{t}",
                                 metadata={"id": str(i)}) for i, t in enumerate(MESSAGES)]
job = client.batches.create(model=MODEL_LITE, src=requests,
                            config=types.CreateBatchJobConfig(display_name="lab7-tickets"))
print(job.name, job.state)
