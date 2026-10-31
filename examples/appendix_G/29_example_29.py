# Додаток Г. Довідник рецептів коду – приклад 29 (рукопис: 93-dodatok-g.md, рядок 559)
import time

reviews = ["Вантаж прибув на день раніше, дякую!", "Третій день не можу додзвонитися."]
job = client.batches.create(
    model="gemini-3.1-flash-lite",
    src=[types.InlinedRequest(contents="Тональність відгуку одним словом:\n" + t) for t in reviews])

FINAL = {types.JobState.JOB_STATE_SUCCEEDED, types.JobState.JOB_STATE_FAILED,
         types.JobState.JOB_STATE_CANCELLED, types.JobState.JOB_STATE_EXPIRED}
while (job := client.batches.get(name=job.name)).state not in FINAL:
    time.sleep(120)                              # опитуємо раз на дві хвилини

if job.state == types.JobState.JOB_STATE_SUCCEEDED:
    for r in job.dest.inlined_responses or []:
        print(r.response.text if r.response else r.error)
