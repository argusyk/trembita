# Розділ 11. Мультимодальне розуміння і структуровані відповіді – приклад 9 (рукопис: 11-multymodalnist.md, рядок 431)
def read_cmr(photo: bytes, declared_total_kg: float | None = None, *, client=None,
             mime_type: str = "image/jpeg", model: str = MODEL_MAIN) -> tuple[Waybill | None, list[str]]:
    """Розбирає фото CMR; повертає (накладна або None, зауваження). Із зауваженнями – людині на перевірку."""
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
    wb = parse_waybill(resp)                       # resp.parsed, інакше валідація resp.text
    if wb is None:                                 # блок, обрив за MAX_TOKENS, невалідний JSON
        return None, ["Модель не повернула накладну за схемою – потрібен ручний розбір"]
    return wb, check_waybill(wb, declared_total_kg)
