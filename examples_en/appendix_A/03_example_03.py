# Appendix A. Laboratory Practicum – example 3 (manuscript: 90-appendix-a.md, line 184)
import time
from google import genai
from google.genai import types
from trembita.costs import cost_from_usage

client = genai.Client()
TASK = "A client bought an annual membership for UAH 14,400 and froze it for 30 days ..."
for level in ("low", "medium", "high"):
    t0 = time.perf_counter()
    resp = client.models.generate_content(
        model="gemini-3.8-flash", contents=TASK,
        config=types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level=level, include_thoughts=True)))
    um = resp.usage_metadata
    print(level, f"{time.perf_counter() - t0:.1f} s", um.thoughts_token_count,
          um.candidates_token_count, f"{cost_from_usage('gemini-3.8-flash', um):.5f}")
