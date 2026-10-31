# Розділ 9. Мислення: рівні, бюджети й підписи думок – приклад 3 (рукопис: 09-myslennia.md, рядок 110)
from google import genai
from google.genai import types

client = genai.Client()
resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Відправлення SM-2610-0388 вийшло зі Львова в понеділок о 18:00. "
             "До Ужгорода 270 км, обмеження для вантажівок 70 км/год, водій має "
             "відпочити 45 хв після 4,5 год їзди. Коли найраніше прибуття?",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high",
                                             include_thoughts=True),
    ),
)
for part in resp.candidates[0].content.parts:
    if not part.text:
        continue                       # частини без тексту (наприклад, лише підпис)
    if part.thought:
        print("[резюме думок]\n", part.text)
    else:
        print("[відповідь]\n", part.text)
