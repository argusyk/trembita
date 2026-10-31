# Додаток А. Практикум – приклад 3 (рукопис: 90-dodatok-a.md, рядок 184)
import time
from google import genai
from google.genai import types
from trembita.costs import cost_from_usage

client = genai.Client()
TASK = "Клієнт купив річний абонемент за 14 400 грн і заморозив його на 30 днів ..."
for level in ("low", "medium", "high"):
    t0 = time.perf_counter()
    resp = client.models.generate_content(
        model="gemini-3.8-flash", contents=TASK,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level=level, include_thoughts=True)))
    um = resp.usage_metadata
    print(level, f"{time.perf_counter() - t0:.1f} с", um.thoughts_token_count,
          um.candidates_token_count, f"{cost_from_usage('gemini-3.8-flash', um):.5f}")
