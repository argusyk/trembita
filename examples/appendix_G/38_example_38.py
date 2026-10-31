# Додаток Г. Довідник рецептів коду – приклад 38 (рукопис: 93-dodatok-g.md, рядок 759)
BLOCKED = {types.FinishReason.SAFETY, types.FinishReason.PROHIBITED_CONTENT,
           types.FinishReason.BLOCKLIST, types.FinishReason.SPII}

def safe_text(resp: types.GenerateContentResponse) -> str:
    fb = resp.prompt_feedback
    if fb is not None and fb.block_reason:           # запит відхилено до генерації
        return f"Запит заблоковано ({fb.block_reason.name}). Зверніться до диспетчера."
    if not resp.candidates:
        return "Відповідь порожня."
    cand = resp.candidates[0]
    if cand.finish_reason in BLOCKED:                # генерацію зупинив фільтр
        return "Відповідь заблоковано фільтром безпеки."
    if cand.finish_reason == types.FinishReason.MAX_TOKENS:
        print("Увага: відповідь обрізано, збільште max_output_tokens")
    return resp.text or ""
