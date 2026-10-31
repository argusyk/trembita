# Розділ 8. Інженерія підказок для Gemini – приклад 3 (рукопис: 08-pidkazky.md, рядок 168)
from google import genai
from google.genai import types

client = genai.Client()
contract = open("dogovir_smereka_kontrahent.txt", encoding="utf-8").read()

prompt = f"""<договір>
{contract}
</договір>

<факти>
Вантаж прийнято 03.10.2026, доставлено 09.10.2026. Маршрут Львів - Вроцлав.
</факти>

Спираючись лише на <договір> і <факти> вище, дай відповідь:
1. Процитуй дослівно пункти договору про строки доставки.
2. Визнач, чи порушено строк. Якщо договір не дає однозначної відповіді, так і скажи.
Формат: спершу цитати, потім висновок одним реченням."""

resp = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=prompt,
    config=types.GenerateContentConfig(
        system_instruction="Ти – юридичний помічник відділу претензій «Смереки».",
    ),
)
print(resp.text)
