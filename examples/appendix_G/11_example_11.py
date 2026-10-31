# Додаток Г. Довідник рецептів коду – приклад 11 (рукопис: 93-dodatok-g.md, рядок 184)
cfg = types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_level="high"))
history = [types.Content(role="user", parts=[types.Part(text="Маршрут Львів – Відень: Чоп чи Краковець?")])]
resp = client.models.generate_content(model="gemini-4-argon", contents=history, config=cfg)

history.append(resp.candidates[0].content)       # правильно: усі частини й підписи
# history.append(types.Content(role="model", parts=[types.Part(text=resp.text)]))  # підписи втрачено

history.append(types.Content(role="user", parts=[types.Part(text="А якщо вантаж ADR?")]))
resp = client.models.generate_content(model="gemini-4-argon", contents=history, config=cfg)
