# Chapter 8. Prompt Engineering for Gemini – example 5 (manuscript: 08-pidkazky.md, line 287)
import json

from google import genai
from google.genai import types

client = genai.Client()
CASES = [json.loads(line) for line in open("claims_test.jsonl", encoding="utf-8")]
# each line: {"text": "...", "label": "damage"}


def accuracy(system: str, model: str = "gemini-3.1-flash-lite") -> float:
    hits = 0
    for case in CASES:
        resp = client.models.generate_content(
            model=model,
            contents=f"Claim: {case['text']}\nCategory:",
            config=types.GenerateContentConfig(
                system_instruction=system, max_output_tokens=256,    # headroom for thoughts, Section 8.3
                thinking_config=types.ThinkingConfig(thinking_level="low")),
        )
        hits += (resp.text or "").strip().lower().rstrip(".") == case["label"]
    return hits / len(CASES)


v1 = "Classify the claim: damage, delay, shortage, documents, other."
v2 = v1 + " If the claim concerns several categories, choose the one that involves money."
for name, prompt in [("v1", v1), ("v2", v2)]:
    print(name, f"{accuracy(prompt):.2f}")
