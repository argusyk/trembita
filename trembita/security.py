"""Базові захисні шари (розділ 19): позначення недовірених даних і грубий фільтр впровадження."""
import re

SUSPICIOUS = [
    r"ignore (all |any )?(previous|prior) instructions",
    r"ігноруй(те)? (усі |всі )?(попередні )?інструкції",
    r"system prompt|системн\w+ (підказк|інструкці)",
    r"надішли .*(пароль|ключ|токен)",
    r"you are now|тепер ти",
]


def looks_like_injection(text: str) -> list[str]:
    """Повертає збіги підозрілих шаблонів (евристика – не заміна Model Armor і людському контролю)."""
    return [p for p in SUSPICIOUS if re.search(p, text, re.I)]


def wrap_untrusted(text: str, source: str) -> str:
    """Обгортає зовнішній вміст тегами, щоб підказка відділяла дані від інструкцій."""
    clean = text.replace("</untrusted>", "")
    return f'<untrusted source="{source}">\n{clean}\n</untrusted>'
