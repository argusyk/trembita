# Chapter 6. The Gemini Model Family and the Open Gemma Models – example 5 (manuscript: 06-rodyna-modeley.md, line 287)
from google import genai

client = genai.Client()

rows = []
for m in client.models.list(config={"page_size": 100}):
    actions = m.supported_actions or []
    if "generateContent" not in actions:
        continue
    rows.append((m.name, m.input_token_limit or 0, m.output_token_limit or 0,
                 bool(m.thinking), "createCachedContent" in actions))

print(f"{'model':42} {'input':>9} {'output':>7} think cache")
for name, inp, out, think, cache in sorted(rows):
    print(f"{name:42} {inp:>9} {out:>7} {think!s:>5} {cache!s:>5}")
