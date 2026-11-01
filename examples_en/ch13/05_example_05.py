# Chapter 13. Optimization: context caching, batch processing and cost – example 5 (manuscript: 13-optymizatsiya.md, line 257)
from google import genai
from google.genai import types
from trembita.config import MODEL_LITE

client = genai.Client()
reviews = ["The cargo arrived a day early, thank you!", "Third day I cannot get through by phone."]
requests = [
    types.InlinedRequest(
        contents="Sentiment of the review in one word (positive/neutral/negative):\n" + text,
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
