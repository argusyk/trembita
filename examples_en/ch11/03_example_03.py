# Chapter 11. Multimodal Understanding and Structured Responses – example 3 (manuscript: 11-multymodalnist.md, line 139)
import time
from google import genai
from google.genai import types

client = genai.Client()

video = client.files.upload(file="lviv_sklad_cam3_2026-10-26.mp4")
while video.state == types.FileState.PROCESSING:     # video is not processed instantly
    time.sleep(10)
    video = client.files.get(name=video.name)
if video.state == types.FileState.FAILED:
    raise RuntimeError(f"File not processed: {video.error}")

clip = types.Part(
    file_data=types.FileData(file_uri=video.uri, mime_type=video.mime_type),
    video_metadata=types.VideoMetadata(
        start_offset="21600s",   # 06:00:00 from the start of the recording
        end_offset="22500s",     # 06:15:00
        fps=2,                   # the forklift moves fast: two frames per second
    ),
)
prompt = (
    "The recording shows the loading of shipment SM-2610-0117 (blue pallets with white markings). "
    "Is there a moment when a pallet is hit or damaged? Give MM:SS timestamps "
    "and describe what is visible. If you are not sure, say so."
)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[clip, prompt],
    config=types.GenerateContentConfig(
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW,
    ),
)
print(resp.text)
