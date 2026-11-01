# Chapter 7. The Gemini API and the Google Gen AI SDK – example 5 (manuscript: 07-api.md, line 225)
from google import genai
from google.genai import types

client = genai.Client()

chat = client.chats.create(
    model="gemini-3.8-flash",
    config=types.GenerateContentConfig(
        system_instruction="You are Trembita. Answer Smereka's dispatchers concisely.",
    ),
)

print(chat.send_message("Shipment SM-2610-0042 is delayed at the border in Chop.").text)
print(chat.send_message("Which customs brokers should be notified?").text)

for item in chat.get_history():          # the whole history: user, model, user, model
    print(item.role, "->", item.parts[0].text[:60])
