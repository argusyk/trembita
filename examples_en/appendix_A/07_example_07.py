# Appendix A. Laboratory Practicum – example 7 (manuscript: 90-appendix-a.md, line 355)
from google import genai
from google.genai import types
from trembita.config import MODEL_LITE

client = genai.Client()
MESSAGES = ["I haven't been able to log in to my email since this morning",
            "The printer on the third floor isn't printing"]
requests = [types.InlinedRequest(contents=f"Request category in one word:\n{t}",
                                 metadata={"id": str(i)}) for i, t in enumerate(MESSAGES)]
job = client.batches.create(model=MODEL_LITE, src=requests,
                            config=types.CreateBatchJobConfig(display_name="lab7-tickets"))
print(job.name, job.state)
