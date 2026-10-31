"""Моделі й ціни «Трембіти» – єдине місце, де названо моделі (розділи 1, 6, 13, 23).

Ідентифікатори – станом на жовтень 2026 року. Кожен можна перевизначити змінною середовища
TREMBITA_MODEL* без зміни коду (міграція, оцінювання, безкоштовний рівень). Аліаси на кшталт
gemini-flash-latest заборонені: оновлення моделі – це свідома зміна з прогоном тестів (розділ 6).
"""
import os
from typing import NamedTuple


def _model(var: str, default: str) -> str:
    """Ідентифікатор моделі зі змінної середовища або значення за замовчуванням."""
    value = os.environ.get(var, default).strip()
    if value.endswith("-latest"):
        raise ValueError(f"{var}={value!r}: аліаси -latest заборонені, закріпіть конкретну версію")
    return value


MODEL_MAIN = _model("TREMBITA_MODEL", "gemini-3.8-flash")               # основна робоча модель
MODEL_SMART = _model("TREMBITA_MODEL_SMART", "gemini-4-argon")          # складні претензії (лише платний рівень)
MODEL_LITE = _model("TREMBITA_MODEL_LITE", "gemini-3.1-flash-lite")     # дешева класифікація, маршрутизатор
MODEL_FALLBACK = _model("TREMBITA_MODEL_FALLBACK", "gemini-3.5-flash")  # резервна Flash, підтримка до 19.05.2027
MODEL_LIVE = _model("TREMBITA_MODEL_LIVE", "gemini-3.8-live")           # голосовий канал для водіїв
MODEL_EMBED = _model("TREMBITA_MODEL_EMBED", "gemini-embedding-2")      # вбудовування для пошуку регламентів
MODEL_IMAGE = _model("TREMBITA_MODEL_IMAGE", "gemini-3.1-flash-image")  # Nano Banana 2: зображення
MODEL_TTS = _model("TREMBITA_MODEL_TTS", "gemini-3.8-flash-tts")        # синтез мовлення


class Price(NamedTuple):
    """Ціни, дол. за 1 млн токенів. cached=None – ціна кешу невідома, рахуємо як звичайний вхід."""
    inp: float
    out: float
    cached: float | None


# ОРІЄНТИРИ на момент написання (жовтень 2026 року), не прайс: звіряйте зі сторінкою цін
# Gemini API перед розрахунками для реального проєкту. Відомі зміни: Argon – за повідомленнями
# 4 / 20 з 01.12.2026; кеш 3.8 Flash – 0,075 і зберігання 1,00 з 01.01.2027.
PRICES: dict[str, Price] = {
    "gemini-4-argon": Price(2.00, 10.00, None),           # [?] до 30.11.2026
    "gemini-3.8-flash": Price(0.75, 3.75, 0.0375),        # вхід/вихід орієнтовно, кеш – до 31.12.2026
    "gemini-3.1-pro-preview": Price(2.00, 12.00, 0.20),   # запити до 200 тис. токенів
    "gemini-3.5-flash-lite": Price(0.30, 2.50, 0.03),     # [?]
    "gemini-3.1-flash-lite": Price(0.25, 1.50, 0.025),    # вхід [?]; вихід і кеш – неперевірені орієнтири
}
CACHE_STORAGE_PER_HOUR = {"gemini-3.8-flash": 0.50}  # дол. за 1 млн токенів за годину (до 31.12.2026)
BATCH_DISCOUNT = 0.5                                  # Batch API: половина ціни
