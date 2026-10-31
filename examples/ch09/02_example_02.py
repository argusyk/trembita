# Розділ 9. Мислення: рівні, бюджети й підписи думок – приклад 2 (рукопис: 09-myslennia.md, рядок 79)
from google.genai import types

# Застарілий спосіб (родина 2.5): числовий бюджет токенів мислення
legacy = types.ThinkingConfig(thinking_budget=-1)        # -1 = динамічний бюджет

# Сучасний спосіб (Gemini 3.x і 4): якісний рівень
modern = types.ThinkingConfig(thinking_level=types.ThinkingLevel.HIGH)

# Помилки на gemini-4-argon (HTTP 400 INVALID_ARGUMENT):
# types.ThinkingConfig(thinking_budget=8192)
# types.ThinkingConfig(thinking_level="minimal")
# types.ThinkingConfig(thinking_budget=1024, thinking_level="low")
