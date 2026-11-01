# Appendix A. Laboratory Practicum – example 6 (manuscript: 90-appendix-a.md, line 313)
from google import genai
from google.genai import types

client = genai.Client()
question = "Which changes to the rules of admission to master's programs took effect this year?"
for tools in ([], [types.Tool(google_search=types.GoogleSearch())]):
    resp = client.models.generate_content(model="gemini-3.8-flash", contents=question,
                                          config=types.GenerateContentConfig(tools=tools))
    print("with search" if tools else "without tools", "|", (resp.text or "")[:300])
    gm = resp.candidates[0].grounding_metadata if resp.candidates else None
    for ch in (gm.grounding_chunks or []) if gm else []:
        if ch.web:
            print(" -", ch.web.title, ch.web.uri)
    print("tool tokens:", resp.usage_metadata.tool_use_prompt_token_count)
