# Додаток Г. Довідник рецептів коду – приклад 8 (рукопис: 93-dodatok-g.md, рядок 128)
SYSTEM = "Ти – «Трембіта», асистент логістичної компанії «Смерека»."
GEN = {"max_output_tokens": 1024, "thinking_level": "low"}

first = client.interactions.create(
    model="gemini-3.8-flash", input="Скільки днів їде вантаж зі Львова до Варшави?",
    system_instruction=SYSTEM, generation_config=GEN)
print(first.status, first.output_text)

follow = client.interactions.create(
    model="gemini-3.8-flash", input="А до Кракова?",
    previous_interaction_id=first.id,        # історію бере сервер
    system_instruction=SYSTEM, generation_config=GEN)
print(follow.output_text, follow.usage.total_output_tokens)
