# Chapter 11. Multimodal Understanding and Structured Responses – example 1 (manuscript: 11-multymodalnist.md, line 42)
from google import genai
from google.genai import types

client = genai.Client()

with open("cmr_SM-2610-0042.jpg", "rb") as f:
    photo = f.read()

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[
        types.Part.from_bytes(
            data=photo,
            mime_type="image/jpeg",
            # small handwritten text: ask for more tokens for this particular photo
            media_resolution=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_HIGH,
        ),
        "What document is this? List the filled-in boxes and mark the illegible ones.",
    ],
)
print(resp.text)
print(resp.usage_metadata.prompt_token_count)   # how much the input cost
