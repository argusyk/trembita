# Chapter 17. Agentic Development: Antigravity, Jules and Gemini Code Assist – example 1 (manuscript: 17-ahentna-rozrobka.md, line 180)
# tests/e2e/test_status_badge.py – a scenario the browser agent checked by hand
import os
import re

from playwright.sync_api import Page, expect

# the address comes from the environment: its own port in the agent's tree, a test stand in CI
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8001")


def test_customs_badge_on_mobile(page: Page) -> None:
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{BASE_URL}/track/SM-2610-0042")
    badge = page.get_by_test_id("status-badge")
    expect(badge).to_have_text("At customs")
    expect(badge).to_have_class(re.compile(r"badge--warning"))
    badge.hover()
    tooltip = page.get_by_role("tooltip")
    expect(tooltip).to_contain_text("Chop")
    # the tooltip fits on the screen and the text is not cut off (no hidden overflow)
    box = tooltip.bounding_box()
    assert box is not None and box["x"] >= 0 and box["x"] + box["width"] <= 390
    assert tooltip.evaluate("el => el.scrollWidth <= el.clientWidth")
