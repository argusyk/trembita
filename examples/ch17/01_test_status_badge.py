# Розділ 17. Агентна розробка: Antigravity, Jules і Gemini Code Assist – приклад 1 (рукопис: 17-ahentna-rozrobka.md, рядок 180)
# tests/e2e/test_status_badge.py – сценарій, який браузерний агент перевірив вручну
import os
import re

from playwright.sync_api import Page, expect

# адресу задає середовище: у дереві агента – його порт, у CI – тестовий стенд
BASE_URL = os.environ.get("BASE_URL", "http://localhost:8001")


def test_customs_badge_on_mobile(page: Page) -> None:
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{BASE_URL}/track/SM-2610-0042")
    badge = page.get_by_test_id("status-badge")
    expect(badge).to_have_text("На митниці")
    expect(badge).to_have_class(re.compile(r"badge--warning"))
    badge.hover()
    tooltip = page.get_by_role("tooltip")
    expect(tooltip).to_contain_text("Чоп")
    # підказка вміщується в екран і текст не обрізано (немає прихованого переповнення)
    box = tooltip.bounding_box()
    assert box is not None and box["x"] >= 0 and box["x"] + box["width"] <= 390
    assert tooltip.evaluate("el => el.scrollWidth <= el.clientWidth")
