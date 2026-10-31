# Розділ 7. Gemini API і Google Gen AI SDK – приклад 2 (рукопис: 07-api.md, рядок 80)
from google import genai
from google.genai import types

client = genai.Client()

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Скільки коштуватиме доставка 20 кг зі Львова до Києва?",
    config=types.GenerateContentConfig(
        system_instruction="Ти – «Трембіта», асистент логістичної компанії «Смерека».",
        max_output_tokens=2048,               # стеля для відповіді
        thinking_config=types.ThinkingConfig(thinking_level="low"),
        stop_sequences=["\n\n---"],           # де примусово зупинитися
        seed=42,                              # для відтворюваних експериментів
        labels={"team": "dispatch"},          # мітки для звітів про витрати
    ),
)
print(resp.text)
