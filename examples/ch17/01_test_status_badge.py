# Розділ 17. Агентна розробка: Antigravity, Jules і Gemini Code Assist – приклад 1 (рукопис: 17-ahentna-rozrobka.md, рядок 180)
# tests/e2e/test_status_badge.py – сценарій, який браузерний агент перевірив вручну
import re

from playwright.sync_api import Page, expect

BASE_URL = "http://localhost:8001"   # порт дерева feat/status-badge


def test_customs_badge_on_mobile(page: Page) -> None:
    page.set_viewport_size({"width": 390, "height": 844})
    page.goto(f"{BASE_URL}/track/SM-2610-0042")
    badge = page.get_by_test_id("status-badge")
    expect(badge).to_have_text("На митниці")
    expect(badge).to_have_class(re.compile(r"badge--warning"))
    # підказка з пунктом пропуску не обрізається на вузькому екрані
    badge.hover()
    expect(page.get_by_role("tooltip")).to_contain_text("Ягодин")
