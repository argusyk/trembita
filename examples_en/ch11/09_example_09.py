# Chapter 11. Multimodal Understanding and Structured Responses – example 9 (manuscript: 11-multymodalnist.md, line 431)
def read_cmr(photo: bytes, declared_total_kg: float | None = None, *, client=None,
             mime_type: str = "image/jpeg", model: str = MODEL_MAIN) -> tuple[Waybill | None, list[str]]:
    """Parses a CMR photo; returns (note or None, remarks). With remarks, it goes to a person for review."""
    from trembita.client import make_client
    image = types.Part.from_bytes(
        data=photo, mime_type=mime_type,
        media_resolution=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_HIGH)
    resp = (client or make_client()).models.generate_content(
        model=model,
        contents=[image, PROMPT],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Waybill,
            thinking_config=types.ThinkingConfig(thinking_level="low"),
        ),
    )
    wb = parse_waybill(resp)                       # resp.parsed, otherwise validation of resp.text
    if wb is None:                                 # block, cut-off at MAX_TOKENS, invalid JSON
        return None, ["The model did not return a note matching the schema – manual parsing needed"]
    return wb, check_waybill(wb, declared_total_kg)
