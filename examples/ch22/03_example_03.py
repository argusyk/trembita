# Розділ 22. Комп'ютерне використання та браузерні агенти – приклад 3 (рукопис: 22-computer-use.md, рядок 157)
import re
from playwright.sync_api import Page

SCROLL_STEP = 600              # пікселів, якщо модель не вказала величину
# Назви клавіш Playwright чутливі до регістру: "ArrowDown", а не "arrowdown" чи "Arrowdown"
KEYS = {"control": "Control", "ctrl": "Control", "alt": "Alt", "shift": "Shift",
        "meta": "Meta", "cmd": "Meta", "enter": "Enter", "return": "Enter", "tab": "Tab",
        "escape": "Escape", "esc": "Escape", "backspace": "Backspace", "delete": "Delete",
        "space": "Space", "home": "Home", "end": "End", "pageup": "PageUp",
        "pagedown": "PageDown", "up": "ArrowUp", "down": "ArrowDown", "left": "ArrowLeft",
        "right": "ArrowRight", "arrowup": "ArrowUp", "arrowdown": "ArrowDown",
        "arrowleft": "ArrowLeft", "arrowright": "ArrowRight"}


def to_playwright_keys(keys) -> str:
    """["control", "a"] або "CONTROL+a" -> "Control+a"; F1–F12 – великими літерами."""
    parts = keys if isinstance(keys, list) else keys.split("+")
    out = []
    for k in (p.strip() for p in parts):
        low = k.lower()
        out.append(KEYS.get(low, k.upper() if re.fullmatch(r"f\d{1,2}", low) else k))
    return "+".join(out)


def scroll_step(args: dict) -> int:
    """3.x: magnitude_in_pixels; 2.5: magnitude у сітці 1000 (як координати)."""
    if "magnitude" in args:
        side = VIEWPORT["height"] if args["direction"] in ("up", "down") else VIEWPORT["width"]
        return int(args["magnitude"] / GRID * side)
    return int(args.get("magnitude_in_pixels", SCROLL_STEP))
