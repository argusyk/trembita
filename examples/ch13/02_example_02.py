# Розділ 13. Оптимізація: кешування контексту, пакетна обробка й вартість – приклад 2 (рукопис: 13-optymizatsiya.md, рядок 103)
from google import genai
from google.genai import types
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION

client = genai.Client()
with open("reglament_smereka.md", encoding="utf-8") as f:
    REGULATIONS = f.read()                     # ~120 тис. токенів, змінюється раз на місяць


def ask_with_regulations(question: str, shift_info: str) -> str:
    resp = client.models.generate_content(
        model=MODEL_MAIN,
        contents=[types.Content(role="user", parts=[
            types.Part(text=REGULATIONS),                  # 1) великий сталий префікс
            types.Part(text=f"{shift_info}\n\n{question}"),  # 2) усе змінне – у кінці
        ])],
        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
    )
    u = resp.usage_metadata
    print(f"вхід: {u.prompt_token_count}, з кешу: {u.cached_content_token_count or 0}")
    return resp.text
