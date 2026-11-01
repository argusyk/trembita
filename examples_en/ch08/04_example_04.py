# Chapter 8. Prompt Engineering for Gemini – example 4 (manuscript: 08-pidkazky.md, line 212)
from google import genai
from google.genai import types

client = genai.Client()


def image(path: str) -> types.Part:
    return types.Part.from_bytes(data=open(path, "rb").read(), mime_type="image/jpeg")


contents = [
    "Photo 1 – CMR consignment note:", image("cmr_SM-2610-0388.jpg"),
    "Photo 2 – seal on the trailer doors:", image("seal_SM-2610-0388.jpg"),
    """Task:
1. Write out the seal number from Photo 1 (the box with the carrier's notes) and from Photo 2.
2. Compare them character by character.
If the number on either photo is illegible, write "not visible", do not guess.
Format: "CMR: ... | Seal: ... | Match: yes/no/unknown".""",
]
resp = client.models.generate_content(model="gemini-3.8-flash", contents=contents)
print(resp.text)
