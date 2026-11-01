# Chapter 7. The Gemini API and the Google Gen AI SDK – example 3 (manuscript: 07-api.md, line 137)
from google import genai
from google.genai import types

client = genai.Client()

history = [
    types.Content(role="user", parts=[types.Part.from_text(text="My name is Iryna, I am a dispatcher.")]),
    types.Content(role="model", parts=[types.Part.from_text(text="Hello, Iryna! How can I help?")]),
    types.Content(role="user", parts=[
        types.Part.from_text(text="What cargo is in the photo, and what is my name?"),
        types.Part.from_bytes(data=open("pallet.jpg", "rb").read(), mime_type="image/jpeg"),
    ]),
]

resp = client.models.generate_content(model="gemini-3.8-flash", contents=history)
print(resp.text)   # the model "remembers" the name because it is in the history sent
