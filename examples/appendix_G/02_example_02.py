# Додаток Г. Довідник рецептів коду – приклад 2 (рукопис: 93-dodatok-g.md, рядок 20)
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Скільки коштуватиме доставка 20 кг зі Львова до Києва?",
    config=types.GenerateContentConfig(
        system_instruction="Ти – «Трембіта», асистент логістичної компанії «Смерека».",
        max_output_tokens=2048,
        thinking_config=types.ThinkingConfig(thinking_level="low"),
    ),
)
print(resp.text)
