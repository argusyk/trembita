# Chapter 22. Computer Use and Browser Agents – example 4 (manuscript: 22-computer-use.md, line 192)
def execute(page: Page, name: str, args: dict) -> None:
    """Executes one predefined action (2.5 and 3.x names)."""
    if name in ("click_at", "click", "right_click"):
        page.mouse.click(*to_pixels(args["x"], args["y"]),
                         button="right" if name == "right_click" else "left")
    elif name == "double_click":
        page.mouse.dblclick(*to_pixels(args["x"], args["y"]))
    elif name in ("hover_at", "move"):
        page.mouse.move(*to_pixels(args["x"], args["y"]))
    elif name == "type_text_at":                     # click + clear + text
        page.mouse.click(*to_pixels(args["x"], args["y"]))
        if args.get("clear_before_typing", True):
            page.keyboard.press("Control+A")
            page.keyboard.press("Delete")
        page.keyboard.type(args["text"])
        if args.get("press_enter", True):
            page.keyboard.press("Enter")
    elif name == "type":                             # text into the focused field
        page.keyboard.type(args["text"])
        if args.get("press_enter"):
            page.keyboard.press("Enter")
    elif name in ("scroll_at", "scroll", "scroll_document"):
        if "x" in args:
            page.mouse.move(*to_pixels(args["x"], args["y"]))
        step = scroll_step(args)
        dx, dy = {"up": (0, -step), "down": (0, step),
                  "left": (-step, 0), "right": (step, 0)}[args["direction"]]
        page.mouse.wheel(dx, dy)
    elif name == "navigate":
        page.goto(args["url"])
    elif name == "go_back":
        page.go_back()
    elif name in ("key_combination", "hotkey", "press_key"):
        page.keyboard.press(to_playwright_keys(args.get("keys") or args["key"]))
    elif name in ("wait_5_seconds", "wait"):
        page.wait_for_timeout(1000 * args.get("seconds", 5))
    elif name != "take_screenshot":                  # a screenshot follows every action anyway
        raise ValueError(f"Unknown action: {name}")
    page.wait_for_load_state()
