# Розділ 8. Інженерія підказок для Gemini – приклад 2 (рукопис: 08-pidkazky.md, рядок 105)
from google import genai
from google.genai import types

client = genai.Client()

LABELS = ("пошкодження", "затримка", "недостача", "документи", "інше")
FEW_SHOT = """Визнач категорію претензії: пошкодження, затримка, недостача, документи, інше.

Претензія: Палета з плиткою приїхала з розбитим кутом, 6 упаковок тріснуті.
Категорія: пошкодження

Претензія: в CMR вказано не ту вагу брутто, митниця не пропускає
Категорія: документи

Претензія: Водій був неввічливий з нашим комірником.
Категорія: інше

Претензія: Замовляли доставку на 12.10, отримали 15.10 без попередження.
Категорія: затримка

Претензія: За накладною 40 коробок, прийняли 37.
Категорія: недостача
"""


def classify(text: str) -> str:
    resp = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents=f"{FEW_SHOT}\nПретензія: {text}\nКатегорія:",
        config=types.GenerateContentConfig(
            # модель мислить: думки теж витрачають max_output_tokens (розділ 7), тож ліміт – із запасом
            thinking_config=types.ThinkingConfig(thinking_level="low"),
            max_output_tokens=256,
        ),
    )
    answer = (resp.text or "").strip().lower().rstrip(".")
    return answer if answer in LABELS else "інше"    # відповідь поза множиною міток – «інше»


print(classify("Водій відмовився чекати розвантаження, товар повезли назад."))
