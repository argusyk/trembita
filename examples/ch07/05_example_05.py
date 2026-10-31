# Розділ 7. Gemini API і Google Gen AI SDK – приклад 5 (рукопис: 07-api.md, рядок 225)
from google import genai
from google.genai import types

client = genai.Client()

chat = client.chats.create(
    model="gemini-3.8-flash",
    config=types.GenerateContentConfig(
        system_instruction="Ти – «Трембіта». Відповідай диспетчерам «Смереки» стисло.",
    ),
)

print(chat.send_message("Вантаж SM-2610-0042 затримується на кордоні в Чопі.").text)
print(chat.send_message("Кого з митних брокерів варто попередити?").text)

for item in chat.get_history():          # уся історія: user, model, user, model
    print(item.role, "->", item.parts[0].text[:60])
