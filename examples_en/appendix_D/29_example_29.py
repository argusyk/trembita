# Appendix D. Code Recipes – example 29 (manuscript: 93-appendix-d.md, line 569)
import time

reviews = ["The shipment arrived a day early, thank you!", "I've been trying to get through for three days."]
job = client.batches.create(
    model="gemini-3.1-flash-lite",
    src=[types.InlinedRequest(contents="Sentiment of the review in one word:\n" + t) for t in reviews])

S = types.JobState
FINAL = {S.JOB_STATE_SUCCEEDED, S.JOB_STATE_PARTIALLY_SUCCEEDED,   # partial success – Agent Platform
         S.JOB_STATE_FAILED, S.JOB_STATE_CANCELLED, S.JOB_STATE_EXPIRED}
while (job := client.batches.get(name=job.name)).state not in FINAL:
    time.sleep(120)                              # poll once every two minutes

if job.state in (S.JOB_STATE_SUCCEEDED, S.JOB_STATE_PARTIALLY_SUCCEEDED) and job.dest:
    for r in job.dest.inlined_responses or []:
        print(r.response.text if r.response else r.error)
