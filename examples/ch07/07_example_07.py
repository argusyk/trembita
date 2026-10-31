# Розділ 7. Gemini API і Google Gen AI SDK – приклад 7 (рукопис: 07-api.md, рядок 316)
from google import genai

client = genai.Client()
SYSTEM = "Ти – «Трембіта», асистент логістичної компанії «Смерека»."
GEN = {"max_output_tokens": 1024, "thinking_level": "low"}

first = client.interactions.create(
    model="gemini-3.8-flash",
    input="Скільки днів їде вантаж зі Львова до Варшави?",
    system_instruction=SYSTEM,
    generation_config=GEN,
)
print(first.status, first.output_text)

# Наступний крок: історію бере сервер, але інструкцію й налаштування передаємо знову
follow = client.interactions.create(
    model="gemini-3.8-flash",
    input="А до Кракова?",
    previous_interaction_id=first.id,
    system_instruction=SYSTEM,
    generation_config=GEN,
)
print(follow.output_text)
print("токени:", follow.usage.total_input_tokens, follow.usage.total_output_tokens)
