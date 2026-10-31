# Розділ 23. Промислова експлуатація на Gemini Enterprise Agent Platform – приклад 5 (рукопис: 23-produkshn.md, рядок 352)
from google.genai import types

# Було (Gemini 2.5 Flash, виведено 20.10.2026):
old_config = types.GenerateContentConfig(
    temperature=0.2,
    thinking_config=types.ThinkingConfig(thinking_budget=1024),
)

# Стало (Gemini 3.8 Flash або 4 Argon):
new_config = types.GenerateContentConfig(
    # temperature не задаємо: для Gemini 3+ рекомендовано типове значення 1.0
    thinking_config=types.ThinkingConfig(thinking_level=types.ThinkingLevel.LOW),
)


def warn_if_retiring(resp) -> None:
    """Пише попередження, якщо сервер повідомив про застарілу модель."""
    st = resp.model_status
    if st and st.model_stage in (types.ModelStage.LEGACY, types.ModelStage.DEPRECATED):
        print(f"Увага: {resp.model_version} – {st.model_stage}, виведення {st.retirement_time}")
