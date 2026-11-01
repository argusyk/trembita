# Chapter 9. Thinking: Levels, Budgets and Thought Signatures – example 2 (manuscript: 09-myslennia.md, line 79)
from google.genai import types

# Legacy way (the 2.5 family): a numeric budget of thinking tokens
legacy = types.ThinkingConfig(thinking_budget=-1)        # -1 = dynamic budget

# Modern way (Gemini 3.x and 4): a qualitative level
modern = types.ThinkingConfig(thinking_level=types.ThinkingLevel.HIGH)

# Errors on gemini-4-argon (HTTP 400 INVALID_ARGUMENT):
# types.ThinkingConfig(thinking_budget=8192)
# types.ThinkingConfig(thinking_level="minimal")
# types.ThinkingConfig(thinking_budget=1024, thinking_level="low")
