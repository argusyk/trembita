"""Моделі й ціни. Ідентифікатори – станом на жовтень 2026 року (розділи 6 і 23)."""
import os

MODEL_MAIN = os.environ.get("TREMBITA_MODEL", "gemini-3.8-flash")    # основна робоча модель
MODEL_SMART = os.environ.get("TREMBITA_MODEL_SMART", "gemini-4-argon")  # складні міркування, агенти
MODEL_LITE = os.environ.get("TREMBITA_MODEL_LITE", "gemini-3.1-flash-lite")  # дешева класифікація
MODEL_LIVE = "gemini-3.8-live"
MODEL_EMBED = "gemini-embedding-2"
MODEL_IMAGE = "gemini-3.1-flash-image"
MODEL_TTS = "gemini-3.8-flash-tts"

# Дол. за 1 млн токенів: (вхід, вихід, кешований вхід). Орієнтири на момент написання –
# звіряйте зі сторінкою цін Gemini API перед розрахунками для реального проєкту.
PRICES = {
    "gemini-4-argon": (2.00, 10.00, 0.20),
    "gemini-3.8-flash": (0.75, 3.75, 0.0375),
    "gemini-3.1-pro-preview": (2.00, 12.00, 0.20),
    "gemini-3.1-flash-lite": (0.25, 1.50, 0.025),
}
CACHE_STORAGE_PER_HOUR = {"gemini-3.8-flash": 0.50}  # дол. за 1 млн токенів за годину
BATCH_DISCOUNT = 0.5
