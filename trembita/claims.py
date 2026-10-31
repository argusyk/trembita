"""Розбір претензії моделлю, що мислить (розділ 9)."""
from google import genai
from google.genai import types
from trembita.config import MODEL_SMART
from trembita.prompts import SYSTEM_INSTRUCTION

CLAIM_INSTRUCTION = SYSTEM_INSTRUCTION + """
Ти допомагаєш юристу відділу претензій. Аналізуй претензію за Конвенцією CMR:
1) які факти підтверджено документами, а які лише заявлено;
2) чи дотримано строки застережень (ст. 30 CMR);
3) межа відповідальності перевізника (ст. 23 CMR) і розрахунок;
4) чого бракує для висновку. Не вигадуй фактів; якщо даних немає – так і пиши.
Це чернетка для юриста, а не остаточне рішення."""

def analyze_claim(client: genai.Client, claim: str, documents: list[str]) -> dict:
    cfg = types.GenerateContentConfig(
        system_instruction=CLAIM_INSTRUCTION,
        thinking_config=types.ThinkingConfig(thinking_level="high", include_thoughts=True),
        max_output_tokens=32_768,              # запас на думки й розлогу відповідь
    )
    parts = [types.Part(text=f"Претензія:\n{claim}")]
    parts += [types.Part(text=f"Документ {i}:\n{d}") for i, d in enumerate(documents, 1)]
    resp = client.models.generate_content(
        model=MODEL_SMART, contents=[types.Content(role="user", parts=parts)], config=cfg)
    content = resp.candidates[0].content
    summary = "\n".join(p.text for p in content.parts if p.thought and p.text)
    um = resp.usage_metadata
    return {"draft": resp.text, "thought_summary": summary,
            "thoughts_tokens": um.thoughts_token_count, "content": content}
