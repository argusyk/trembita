# Chapter 14. The Live API and media generation – example 7 (manuscript: 14-live-media.md, line 337)
import os
import time
from google import genai
from google.genai import types

client = genai.Client()
VEO_MODEL = os.environ["VEO_MODEL"]       # current Veo 3.1 ID, from client.models.list()

op = client.models.generate_videos(
    model=VEO_MODEL,
    prompt="A lorry with a green fir tree on its tarpaulin drives along a mountain road in the Carpathians "
           "at dawn, the camera glides smoothly above the road",
    config=types.GenerateVideosConfig(aspect_ratio="16:9",
                                      negative_prompt="text, third-party logos, people in frame"),
)
while not op.done:
    time.sleep(20)                         # generation takes minutes
    op = client.operations.get(op)

video = op.response.generated_videos[0]
client.files.download(file=video.video)
video.video.save("smereka_karpaty.mp4")
