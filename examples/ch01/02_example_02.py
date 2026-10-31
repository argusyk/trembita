# Розділ 1. Що таке Gemini: Google DeepMind, екосистема й наскрізний приклад – приклад 2 (рукопис: 01-vstup-gemini.md, рядок 198)
from google import genai
from google.genai import types

client = genai.Client()  # читає GEMINI_API_KEY із середовища

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Клієнт питає: скільки днів їде вантаж зі Львова до Варшави?",
    config=types.GenerateContentConfig(
        system_instruction=(
            "Ти – «Трембіта», асистент логістичної компанії «Смерека». "
            "Відповідай українською, коротко й ввічливо. "
            "Якщо не маєш точних даних, прямо скажи про це."
        ),
        max_output_tokens=1024,
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
)
print(response.text)
