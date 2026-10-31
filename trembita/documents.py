"""Читання накладної CMR зі структурованою відповіддю (розділ 11)."""
import re
from datetime import date
from google.genai import types
from trembita.client import make_client
from trembita.config import MODEL_MAIN
from trembita.schemas import Waybill

PROMPT = ("Це фото накладної CMR. Заповни схему за графами бланка. "
          "Дату подай як РРРР-ММ-ДД. Вагу бери з графи 11 (брутто). "
          "Нерозбірливе не вгадуй: залиш порожній рядок.")

def read_cmr(photo: bytes, declared_total_kg: float | None = None) -> tuple[Waybill, list[str]]:
    client = make_client()
    image = types.Part.from_bytes(
        data=photo, mime_type="image/jpeg",
        media_resolution=types.PartMediaResolutionLevel.MEDIA_RESOLUTION_HIGH)
    resp = client.models.generate_content(
        model=MODEL_MAIN,
        contents=[image, PROMPT],
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=Waybill,
            thinking_config=types.ThinkingConfig(thinking_level="low"),
        ),
    )
    wb: Waybill = resp.parsed
    issues = []                                   # змістові перевірки після схеми
    if not re.fullmatch(r"[A-Z]{2}\s?\d{4,}", wb.number.replace("-", "")):
        issues.append(f"Підозрілий номер CMR: {wb.number!r}")
    if wb.date and wb.date > date.today().isoformat():
        issues.append(f"Дата з майбутнього: {wb.date}")
    total = sum(i.weight_kg for i in wb.items)
    if declared_total_kg and abs(total - declared_total_kg) > 0.02 * declared_total_kg:
        issues.append(f"Вага {total} кг не збігається із заявленою {declared_total_kg} кг")
    if any(not field for field in (wb.sender, wb.consignee, wb.origin, wb.destination)):
        issues.append("Порожні графи сторін або місць – потрібне підтвердження")
    return wb, issues
