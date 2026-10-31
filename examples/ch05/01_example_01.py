# Розділ 5. Безпека й вирівнювання в Google DeepMind – приклад 1 (рукопис: 05-bezpeka-vyrivniuvannia.md, рядок 90)
from google import genai
from google.genai import types

from trembita.config import MODEL_MAIN

client = genai.Client()

# Відділ претензій: гнівні листи й питання ADR – легітимна робота
claims_safety = [
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_HARASSMENT,
        threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
    types.SafetySetting(
        category=types.HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT,
        threshold=types.HarmBlockThreshold.BLOCK_ONLY_HIGH,
    ),
]

resp = client.models.generate_content(
    model=MODEL_MAIN,
    contents="Стисло підсумуй претензію клієнта до SM-2610-0042: ...",
    config=types.GenerateContentConfig(safety_settings=claims_safety),
)
