# Розділ 1. Що таке Gemini: Google DeepMind, екосистема й наскрізний приклад – приклад 1 (рукопис: 01-vstup-gemini.md, рядок 126)
from google import genai

client = genai.Client()  # ключ береться зі змінної GEMINI_API_KEY
first = client.interactions.create(
    model="gemini-3.8-flash",
    input="Які документи потрібні для перевезення вантажу до Польщі?",
)
print(first.output_text)

# продовження розмови: історію сервер підставить сам
follow = client.interactions.create(
    model="gemini-3.8-flash",
    input="А якщо вантаж небезпечний?",
    previous_interaction_id=first.id,
)
print(follow.output_text)
