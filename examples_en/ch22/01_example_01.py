# Chapter 22. Computer Use and Browser Agents – example 1 (manuscript: 22-computer-use.md, line 67)
GRID = 1000                                  # the model's virtual grid
VIEWPORT = {"width": 1280, "height": 720}    # the real browser window


def to_pixels(x: int, y: int) -> tuple[int, int]:
    """The model's normalized coordinates -> window pixels, clamped to the bounds."""
    px = int(x / GRID * VIEWPORT["width"])
    py = int(y / GRID * VIEWPORT["height"])
    return min(px, VIEWPORT["width"] - 1), min(py, VIEWPORT["height"] - 1)
