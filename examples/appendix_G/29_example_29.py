# Додаток Г. Довідник рецептів коду – приклад 29 (рукопис: 93-dodatok-g.md, рядок 569)
import time

reviews = ["Вантаж прибув на день раніше, дякую!", "Третій день не можу додзвонитися."]
job = client.batches.create(
    model="gemini-3.1-flash-lite",
    src=[types.InlinedRequest(contents="Тональність відгуку одним словом:\n" + t) for t in reviews])

S = types.JobState
FINAL = {S.JOB_STATE_SUCCEEDED, S.JOB_STATE_PARTIALLY_SUCCEEDED,   # частковий успіх – Agent Platform
         S.JOB_STATE_FAILED, S.JOB_STATE_CANCELLED, S.JOB_STATE_EXPIRED}
while (job := client.batches.get(name=job.name)).state not in FINAL:
    time.sleep(120)                              # опитуємо раз на дві хвилини

if job.state in (S.JOB_STATE_SUCCEEDED, S.JOB_STATE_PARTIALLY_SUCCEEDED) and job.dest:
    for r in job.dest.inlined_responses or []:
        print(r.response.text if r.response else r.error)
