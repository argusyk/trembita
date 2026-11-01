# Chapter 19. Application Security and Risks – example 5 (manuscript: 19-bezpeka-zastosunkiv.md, line 283)
def answer_from_policy(question: str, policy: str, *, client=None, model: str = MODEL_MAIN) -> str:
    resp = (client or make_client()).models.generate_content(
        model=model,
        contents=f"Policy:\n{policy}\n\nCustomer question: {question}",
        config=types.GenerateContentConfig(
            system_instruction=POLICY_INSTRUCTION,
            response_mime_type="application/json",
            response_schema=GroundedAnswer,
        ),
    )
    ga = resp.parsed if isinstance(resp.parsed, GroundedAnswer) else None   # None: block, cut-off, invalid JSON
    return verify_grounded(ga, policy) or ESCALATION
