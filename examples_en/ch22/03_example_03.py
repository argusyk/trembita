# Chapter 22. Computer Use and Browser Agents – example 3 (manuscript: 22-computer-use.md, line 157)
import re
from playwright.sync_api import Page

SCROLL_STEP = 600              # pixels, if the model did not specify an amount
# Playwright key names are case-sensitive: "ArrowDown", not "arrowdown" or "Arrowdown"
KEYS = {"control": "Control", "ctrl": "Control", "alt": "Alt", "shift": "Shift",
        "meta": "Meta", "cmd": "Meta", "enter": "Enter", "return": "Enter", "tab": "Tab",
        "escape": "Escape", "esc": "Escape", "backspace": "Backspace", "delete": "Delete",
        "space": "Space", "home": "Home", "end": "End", "pageup": "PageUp",
        "pagedown": "PageDown", "up": "ArrowUp", "down": "ArrowDown", "left": "ArrowLeft",
        "right": "ArrowRight", "arrowup": "ArrowUp", "arrowdown": "ArrowDown",
        "arrowleft": "ArrowLeft", "arrowright": "ArrowRight"}


def to_playwright_keys(keys) -> str:
    """["control", "a"] or "CONTROL+a" -> "Control+a"; F1–F12 in upper case."""
    parts = keys if isinstance(keys, list) else keys.split("+")
    out = []
    for k in (p.strip() for p in parts):
        low = k.lower()
        out.append(KEYS.get(low, k.upper() if re.fullmatch(r"f\d{1,2}", low) else k))
    return "+".join(out)


def scroll_step(args: dict) -> int:
    """3.x: magnitude_in_pixels; 2.5: magnitude on the 1000 grid (like coordinates)."""
    if "magnitude" in args:
        side = VIEWPORT["height"] if args["direction"] in ("up", "down") else VIEWPORT["width"]
        return int(args["magnitude"] / GRID * side)
    return int(args.get("magnitude_in_pixels", SCROLL_STEP))
