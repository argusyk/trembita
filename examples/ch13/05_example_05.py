# Розділ 13. Оптимізація: кешування контексту, пакетна обробка й вартість – приклад 5 (рукопис: 13-optymizatsiya.md, рядок 256)
import json
import time
from google import genai
from google.genai import types
from trembita.config import MODEL_MAIN

client = genai.Client()
claims = [{"id": "SM-2610-0042", "text": "Пошкоджено два палети при розвантаженні..."}]

with open("claims.jsonl", "w", encoding="utf-8") as f:
    for c in claims:
        line = {"key": c["id"], "request": {
            "contents": [{"role": "user", "parts": [{"text": "Стисло підсумуй претензію:\n" + c["text"]}]}]}}
        f.write(json.dumps(line, ensure_ascii=False) + "\n")

src = client.files.upload(file="claims.jsonl",
                          config=types.UploadFileConfig(display_name="claims", mime_type="jsonl"))
job = client.batches.create(model=MODEL_MAIN, src=src.name)

FINAL = {types.JobState.JOB_STATE_SUCCEEDED, types.JobState.JOB_STATE_FAILED,
         types.JobState.JOB_STATE_CANCELLED, types.JobState.JOB_STATE_EXPIRED}
while (job := client.batches.get(name=job.name)).state not in FINAL:
    time.sleep(120)                          # опитуємо раз на дві хвилини, не частіше

if job.state == types.JobState.JOB_STATE_SUCCEEDED:
    raw = client.files.download(file=job.dest.file_name)
    for row in raw.decode("utf-8").splitlines():
        item = json.loads(row)
        print(item["key"], "->", "error" in item and item["error"] or "готово")
