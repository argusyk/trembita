# Розділ 5. Безпека й вирівнювання в Google DeepMind – приклад 2 (рукопис: 05-bezpeka-vyrivniuvannia.md, рядок 121)
def explain_block(resp: types.GenerateContentResponse) -> str | None:
    """Повертає опис блокування або None, якщо відповідь нормальна."""
    fb = resp.prompt_feedback
    if fb is not None and fb.block_reason is not None:
        return f"запит заблоковано: {fb.block_reason.name}"
    if not resp.candidates:
        return "немає кандидатів"
    cand = resp.candidates[0]
    if cand.finish_reason == types.FinishReason.SAFETY:
        hits = [r.category.name for r in (cand.safety_ratings or []) if r.blocked]
        return f"відповідь заблоковано фільтром: {', '.join(hits) or '?'}"
    if cand.finish_reason in (types.FinishReason.PROHIBITED_CONTENT,
                              types.FinishReason.BLOCKLIST,
                              types.FinishReason.SPII):
        return f"відповідь зупинено: {cand.finish_reason.name}"
    return None

reason = explain_block(resp)
if reason:
    print("Не вдалося відповісти автоматично; передаю диспетчеру.", reason)
else:
    print(resp.text)
