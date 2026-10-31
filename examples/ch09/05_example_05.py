# Розділ 9. Мислення: рівні, бюджети й підписи думок – приклад 5 (рукопис: 09-myslennia.md, рядок 173)
from google import genai
from google.genai import types

client = genai.Client()
cfg = types.GenerateContentConfig(thinking_config=types.ThinkingConfig(thinking_level="high"))
history = [types.Content(role="user", parts=[types.Part(text="Порівняй маршрути Львів–Відень "
                                                         "через Чоп і через Краковець.")])]
resp = client.models.generate_content(model="gemini-4-argon", contents=history, config=cfg)

# Правильно: додаємо content моделі цілком – з усіма частинами й підписами
history.append(resp.candidates[0].content)

# Неправильно: відтворюємо репліку з тексту – підписи втрачено
# history.append(types.Content(role="model", parts=[types.Part(text=resp.text)]))

signed = [p for p in resp.candidates[0].content.parts if p.thought_signature]
print("частин із підписом:", len(signed))

history.append(types.Content(role="user", parts=[types.Part(text="А якщо вантаж небезпечний (ADR)?")]))
resp = client.models.generate_content(model="gemini-4-argon", contents=history, config=cfg)
