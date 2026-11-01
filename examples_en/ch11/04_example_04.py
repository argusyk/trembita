# Chapter 11. Multimodal Understanding and Structured Responses – example 4 (manuscript: 11-multymodalnist.md, line 188)
from google import genai

client = genai.Client()

call = client.files.upload(file="dzvinok_vodiy_2610_2347.mp3")
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=[
        call,
        "Transcribe the conversation in Ukrainian with timestamps [MM:SS] and labels "
        "'Dispatcher' / 'Driver'. Then, as a separate list, write out: shipment number, "
        "location, problem, what was agreed. Mark illegible passages as [inaudible].",
    ],
)
print(resp.text)
