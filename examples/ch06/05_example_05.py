# Розділ 6. Родина моделей Gemini і відкриті моделі Gemma – приклад 5 (рукопис: 06-rodyna-modeley.md, рядок 273)
from google import genai

client = genai.Client()

rows = []
for m in client.models.list(config={"page_size": 100}):
    actions = m.supported_actions or []
    if "generateContent" not in actions:
        continue
    rows.append((m.name, m.input_token_limit or 0, m.output_token_limit or 0,
                 bool(m.thinking), "createCachedContent" in actions))

print(f"{'модель':42} {'вхід':>9} {'вихід':>7} мисл. кеш")
for name, inp, out, think, cache in sorted(rows):
    print(f"{name:42} {inp:>9} {out:>7} {think!s:>5} {cache!s:>5}")
