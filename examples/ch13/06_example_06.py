# Розділ 13. Оптимізація: кешування контексту, пакетна обробка й вартість – приклад 6 (рукопис: 13-optymizatsiya.md, рядок 319)
from google.genai import types
from trembita.prompts import SYSTEM_INSTRUCTION

QUICK_REPLY = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION + "\nВідповідай коротко: до трьох речень.",
    max_output_tokens=1024,                                   # стеля із запасом
    thinking_config=types.ThinkingConfig(thinking_level="low"),
    media_resolution=types.MediaResolution.MEDIA_RESOLUTION_MEDIUM,
)
