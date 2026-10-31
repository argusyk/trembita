# Розділ 14. Live API і генерація медіа – приклад 7 (рукопис: 14-live-media.md, рядок 337)
import os
import time
from google import genai
from google.genai import types

client = genai.Client()
VEO_MODEL = os.environ["VEO_MODEL"]       # актуальний ID Veo 3.1 – з client.models.list()

op = client.models.generate_videos(
    model=VEO_MODEL,
    prompt="Вантажівка із зеленою ялинкою на тенті їде серпантином у Карпатах на світанку, "
           "камера плавно пролітає над дорогою",
    config=types.GenerateVideosConfig(aspect_ratio="16:9",
                                      negative_prompt="текст, чужі логотипи, люди в кадрі"),
)
while not op.done:
    time.sleep(20)                         # генерація триває хвилини
    op = client.operations.get(op)

video = op.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("smereka_karpaty.mp4")
