# Chapter 13. Optimization: context caching, batch processing and cost – example 7 (manuscript: 13-optymizatsiya.md, line 348)
from google.genai import types
from trembita.prompts import SYSTEM_INSTRUCTION

QUICK_REPLY = types.GenerateContentConfig(
    system_instruction=SYSTEM_INSTRUCTION + "\nAnswer briefly: no more than three sentences.",
    max_output_tokens=1024,                                   # ceiling with a margin
    thinking_config=types.ThinkingConfig(thinking_level="low"),
    media_resolution=types.MediaResolution.MEDIA_RESOLUTION_MEDIUM,
)
