# Розділ 19. Безпека застосунків і ризики – приклад 3 (рукопис: 19-bezpeka-zastosunkiv.md, рядок 149)
import logging
from google.genai import types

log = logging.getLogger("trembita.safety")
BLOCKED = {types.FinishReason.SAFETY, types.FinishReason.PROHIBITED_CONTENT,
           types.FinishReason.BLOCKLIST, types.FinishReason.SPII}

def safe_text(resp: types.GenerateContentResponse) -> str:
    fb = resp.prompt_feedback
    if fb is not None and fb.block_reason:            # запит відхилено до генерації
        log.warning("prompt blocked: %s", fb.block_reason)
        return "Не можу опрацювати цей запит. Зверніться, будь ласка, до диспетчера."
    if not resp.candidates:
        return "Відповідь порожня. Спробуйте переформулювати запитання."
    cand = resp.candidates[0]
    if cand.finish_reason in BLOCKED:                 # генерацію зупинив фільтр
        hits = [r.category for r in (cand.safety_ratings or []) if r.blocked]
        log.warning("response blocked: %s %s", cand.finish_reason, hits)
        return "Відповідь заблоковано фільтром безпеки. Запит передано диспетчеру."
    return resp.text or ""
