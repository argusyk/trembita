# Chapter 3. Tokens, Multimodal Tokens and Long Context – example 3 (manuscript: 03-tokeny-kontekst.md, line 202)
from pathlib import Path
from google import genai
from google.genai import types

client = genai.Client()
scan = Path("cmr_SM-2610-0042.jpg").read_bytes()
levels = ["MEDIA_RESOLUTION_LOW", "MEDIA_RESOLUTION_MEDIUM", "MEDIA_RESOLUTION_HIGH"]

for level in levels:
    # resolution is set for a specific part of the request (Gemini 3 and newer)
    image = types.Part.from_bytes(data=scan, mime_type="image/jpeg",
                                  media_resolution=level)
    resp = client.models.count_tokens(
        model="gemini-3.8-flash",
        contents=[image, "Read the consignment note number in box 4."],
    )
    print(level, resp.total_tokens)
