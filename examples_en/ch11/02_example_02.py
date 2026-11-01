# Chapter 11. Multimodal Understanding and Structured Responses – example 2 (manuscript: 11-multymodalnist.md, line 98)
from google import genai
from google.genai import types

client = genai.Client()

contract = client.files.upload(
    file="dohovir_perevezennia_2026.pdf",
    config=types.UploadFileConfig(display_name="Contract Smereka – Karpaty Agro LLC"),
)

question = (
    "Find the clauses on the carrier's liability for damage to cargo. "
    "For each, give the page and clause number and quote the key sentence."
)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[contract, question],      # the SDK turns the File object into file_data
    config=types.GenerateContentConfig(
        media_resolution=types.MediaResolution.MEDIA_RESOLUTION_MEDIUM,
    ),
)
print(resp.text)
