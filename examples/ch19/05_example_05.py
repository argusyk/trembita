# Розділ 19. Безпека застосунків і ризики – приклад 5 (рукопис: 19-bezpeka-zastosunkiv.md, рядок 283)
def answer_from_policy(question: str, policy: str, *, client=None, model: str = MODEL_MAIN) -> str:
    resp = (client or make_client()).models.generate_content(
        model=model,
        contents=f"Регламент:\n{policy}\n\nПитання клієнта: {question}",
        config=types.GenerateContentConfig(
            system_instruction=POLICY_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=GroundedAnswer,
        ),
    )
    ga = resp.parsed if isinstance(resp.parsed, GroundedAnswer) else None   # None: блок, обрив, невалідний JSON
    return verify_grounded(ga, policy) or ESCALATION
