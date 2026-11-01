# Chapter 13. Optimization: context caching, batch processing and cost – example 2 (manuscript: 13-optymizatsiya.md, line 117)
from google import genai
from google.genai import types
from trembita.config import MODEL_MAIN
from trembita.prompts import SYSTEM_INSTRUCTION

client = genai.Client()
with open("reglament_smereka.md", encoding="utf-8") as f:
    REGULATIONS = f.read()                     # ~120K tokens, changes once a month


def ask_with_regulations(question: str, shift_info: str) -> str:
    resp = client.models.generate_content(
        model=MODEL_MAIN,
        contents=[types.Content(role="user", parts=[
            types.Part(text=REGULATIONS),                  # 1) large stable prefix
            types.Part(text=f"{shift_info}\n\n{question}"),  # 2) everything variable goes last
        ])],
        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION),
    )
    u = resp.usage_metadata
    print(f"input: {u.prompt_token_count}, from cache: {u.cached_content_token_count or 0}")
    return resp.text
