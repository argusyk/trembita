# Appendix D. Code Recipes – example 19 (manuscript: 93-appendix-d.md, line 347)
import time

video = client.files.upload(file="lviv_sklad_cam3_2026-10-26.mp4")
while video.state == types.FileState.PROCESSING:
    time.sleep(10)
    video = client.files.get(name=video.name)

clip = types.Part(
    file_data=types.FileData(file_uri=video.uri, mime_type=video.mime_type),
    # public YouTube: types.FileData(file_uri="https://www.youtube.com/watch?v=...")
    video_metadata=types.VideoMetadata(start_offset="21600s", end_offset="22500s", fps=2),
)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[clip, "Was a pallet hit during loading? Give timestamps as MM:SS."],
    config=types.GenerateContentConfig(media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW),
)
