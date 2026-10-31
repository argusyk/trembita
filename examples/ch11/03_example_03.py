# Розділ 11. Мультимодальне розуміння і структуровані відповіді – приклад 3 (рукопис: 11-multymodalnist.md, рядок 139)
import time
from google import genai
from google.genai import types

client = genai.Client()

video = client.files.upload(file="lviv_sklad_cam3_2026-10-26.mp4")
while video.state == types.FileState.PROCESSING:     # відео обробляється не миттєво
    time.sleep(10)
    video = client.files.get(name=video.name)
if video.state == types.FileState.FAILED:
    raise RuntimeError(f"Файл не оброблено: {video.error}")

clip = types.Part(
    file_data=types.FileData(file_uri=video.uri, mime_type=video.mime_type),
    video_metadata=types.VideoMetadata(
        start_offset="21600s",   # 06:00:00 від початку запису
        end_offset="22500s",     # 06:15:00
        fps=2,                   # навантажувач рухається швидко: два кадри на секунду
    ),
)
prompt = (
    "На записі – навантаження відправлення SM-2610-0042 (сині палети з білим маркуванням). "
    "Чи є момент, коли палету вдарено або пошкоджено? Вкажи мітки часу ХХ:СС "
    "і опиши, що видно. Якщо впевненості немає, так і напиши."
)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[clip, prompt],
    config=types.GenerateContentConfig(
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_LOW,
    ),
)
print(resp.text)
