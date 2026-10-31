# Розділ 22. Комп'ютерне використання та браузерні агенти – приклад 1 (рукопис: 22-computer-use.md, рядок 67)
GRID = 1000                                  # віртуальна сітка моделі
VIEWPORT = {"width": 1280, "height": 720}    # реальне вікно браузера


def to_pixels(x: int, y: int) -> tuple[int, int]:
    """Нормовані координати моделі -> пікселі вікна, з обмеженням межами."""
    px = int(x / GRID * VIEWPORT["width"])
    py = int(y / GRID * VIEWPORT["height"])
    return min(px, VIEWPORT["width"] - 1), min(py, VIEWPORT["height"] - 1)
