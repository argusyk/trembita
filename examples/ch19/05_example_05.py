# Розділ 19. Безпека застосунків і ризики – приклад 5 (рукопис: 19-bezpeka-zastosunkiv.md, рядок 221)
import re
from urllib.parse import urlparse

ALLOWED = ("smereka.ua",)                       # лише власні домени компанії
MD_LINK = re.compile(r"(!?)\[([^\]]*)\]\(([^)\s]+)[^)]*\)")
BARE_URL = re.compile(r"https?://[^\s)>\]]+")

def _trusted(url: str) -> bool:
    host = (urlparse(url).hostname or "").lower()
    return any(host == d or host.endswith("." + d) for d in ALLOWED)

def sanitize_output(text: str) -> str:
    def md(m: re.Match) -> str:
        is_image, label, url = m.group(1), m.group(2), m.group(3)
        if is_image:                              # жодних зовнішніх зображень
            return f"[зображення вилучено: {label}]"
        return m.group(0) if _trusted(url) else f"{label} [посилання вилучено]"
    text = MD_LINK.sub(md, text)
    return BARE_URL.sub(lambda m: m.group(0) if _trusted(m.group(0)) else "[URL вилучено]", text)
