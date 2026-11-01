# Chapter 5. Safety and Alignment at Google DeepMind – example 1 (manuscript: 05-bezpeka-vyrivniuvannia.md, line 90)
from google import genai
from google.genai import types

from trembita.config import MODEL_MAIN

client = genai.Client()

# Claims department: angry emails and ADR questions are legitimate work
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
    contents="Briefly summarize the customer's claim regarding SM-2610-0117: ...",
    config=types.GenerateContentConfig(safety_settings=claims_safety),
)
