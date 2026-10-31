# Додаток Г. Довідник рецептів коду – приклад 5 (рукопис: 93-dodatok-g.md, рядок 74)
chat = client.chats.create(
    model="gemini-3.8-flash",
    config=types.GenerateContentConfig(system_instruction="Ти – «Трембіта». Відповідай стисло."),
)
print(chat.send_message("Вантаж SM-2610-0042 затримується в Чопі.").text)
print(chat.send_message("Кого з митних брокерів попередити?").text)

for item in chat.get_history():              # user, model, user, model
    print(item.role, "->", (item.parts[0].text or "")[:60])
