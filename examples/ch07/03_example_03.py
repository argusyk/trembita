# Розділ 7. Gemini API і Google Gen AI SDK – приклад 3 (рукопис: 07-api.md, рядок 137)
from google import genai
from google.genai import types

client = genai.Client()

history = [
    types.Content(role="user", parts=[types.Part.from_text(text="Мене звати Ірина, я диспетчерка.")]),
    types.Content(role="model", parts=[types.Part.from_text(text="Вітаю, Ірино! Чим допомогти?")]),
    types.Content(role="user", parts=[
        types.Part.from_text(text="Що за вантаж на фото і як мене звати?"),
        types.Part.from_bytes(data=open("pallet.jpg", "rb").read(), mime_type="image/jpeg"),
    ]),
]

resp = client.models.generate_content(model="gemini-3.8-flash", contents=history)
print(resp.text)   # модель «пам'ятає» ім'я, бо воно є в переданій історії
