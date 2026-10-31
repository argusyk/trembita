# Розділ 8. Інженерія підказок для Gemini – приклад 5 (рукопис: 08-pidkazky.md, рядок 287)
import json

from google import genai
from google.genai import types

client = genai.Client()
CASES = [json.loads(line) for line in open("claims_test.jsonl", encoding="utf-8")]
# кожен рядок: {"text": "...", "label": "пошкодження"}


def accuracy(system: str, model: str = "gemini-3.1-flash-lite") -> float:
    hits = 0
    for case in CASES:
        resp = client.models.generate_content(
            model=model,
            contents=f"Претензія: {case['text']}\nКатегорія:",
            config=types.GenerateContentConfig(
                system_instruction=system, max_output_tokens=256,    # запас на думки, підрозділ 8.3
                thinking_config=types.ThinkingConfig(thinking_level="low")),
        )
        hits += (resp.text or "").strip().lower().rstrip(".") == case["label"]
    return hits / len(CASES)


v1 = "Класифікуй претензію: пошкодження, затримка, недостача, документи, інше."
v2 = v1 + " Якщо претензія стосується кількох категорій, обери ту, що стосується грошей."
for name, prompt in [("v1", v1), ("v2", v2)]:
    print(name, f"{accuracy(prompt):.2f}")
