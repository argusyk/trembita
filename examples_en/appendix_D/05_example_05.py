# Appendix D. Code Recipes – example 5 (manuscript: 93-appendix-d.md, line 74)
chat = client.chats.create(
    model="gemini-3.8-flash",
    config=types.GenerateContentConfig(system_instruction="You are Trembita. Answer concisely."),
)
print(chat.send_message("Shipment SM-2610-0042 is delayed in Chop.").text)
print(chat.send_message("Which customs brokers should be warned?").text)

for item in chat.get_history():              # user, model, user, model
    print(item.role, "->", (item.parts[0].text or "")[:60])
