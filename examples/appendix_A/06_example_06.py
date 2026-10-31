# Додаток А. Практикум – приклад 6 (рукопис: 90-dodatok-a.md, рядок 293)
from google import genai
from google.genai import types

client = genai.Client()
question = "Які зміни в правилах вступу до магістратури набули чинності цього року?"
for tools in ([], [types.Tool(google_search=types.GoogleSearch())]):
    resp = client.models.generate_content(model="gemini-3.8-flash", contents=question,
                                          config=types.GenerateContentConfig(tools=tools))
    print("з пошуком" if tools else "без інструментів", "|", (resp.text or "")[:300])
    gm = resp.candidates[0].grounding_metadata
    for ch in (gm.grounding_chunks or []) if gm else []:
        if ch.web:
            print(" -", ch.web.title, ch.web.uri)
    print("токени інструментів:", resp.usage_metadata.tool_use_prompt_token_count)
