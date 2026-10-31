"""Розбір претензії моделлю, що мислить (розділ 9)."""
from google import genai
from google.genai import types

from .config import MODEL_SMART
from .prompts import SYSTEM_INSTRUCTION

CLAIM_INSTRUCTION = SYSTEM_INSTRUCTION + """
Ти допомагаєш юристу відділу претензій. Аналізуй претензію за Конвенцією CMR:
1) які факти підтверджено документами, а які лише заявлено;
2) чи дотримано строки застережень (ст. 30 CMR);
3) межа відповідальності перевізника (ст. 23 CMR) і розрахунок;
4) чого бракує для висновку. Не вигадуй фактів; якщо даних немає – так і пиши.
Це чернетка для юриста, а не остаточне рішення."""


def analyze_claim(client: genai.Client, claim: str, documents: list[str], *, model: str = MODEL_SMART) -> dict:
    """Чернетка аналізу претензії, резюме думок і вміст відповіді (для уточнень у тій самій розмові)."""
    cfg = types.GenerateContentConfig(
        system_instruction=CLAIM_INSTRUCTION,
        thinking_config=types.ThinkingConfig(thinking_level="high", include_thoughts=True),
        max_output_tokens=32_768,              # запас на думки й розлогу відповідь
    )
    parts = [types.Part(text=f"Претензія:\n{claim}")]
    parts += [types.Part(text=f"Документ {i}:\n{d}") for i, d in enumerate(documents, 1)]
    resp = client.models.generate_content(
        model=model, contents=[types.Content(role="user", parts=parts)], config=cfg)
    um = resp.usage_metadata
    thoughts_tokens = (um.thoughts_token_count or 0) if um else 0
    cand = resp.candidates[0] if resp.candidates else None
    content = cand.content if cand else None
    if content is None:                        # блок запиту чи порожня відповідь
        return {"draft": "", "thought_summary": "", "thoughts_tokens": thoughts_tokens, "content": None,
                "finish_reason": getattr(cand, "finish_reason", None)}
    summary = "\n".join(p.text for p in (content.parts or []) if p.thought and p.text)
    return {"draft": resp.text or "", "thought_summary": summary, "thoughts_tokens": thoughts_tokens,
            "content": content, "finish_reason": cand.finish_reason}
