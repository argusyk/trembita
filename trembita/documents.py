"""Читання накладної CMR зі структурованою відповіддю (розділ 11).

read_cmr() робить запит до моделі; змістові перевірки винесено в чисті функції
(check_waybill, looks_like_cmr_number), які тестуються без мережі.
"""
import re
from datetime import date

from google.genai import types
from pydantic import ValidationError

from .config import MODEL_MAIN
from .schemas import Waybill

PROMPT = ("Це фото накладної CMR. Заповни схему за графами бланка. "
          "Дату подай як РРРР-ММ-ДД. Вагу бери з графи 11 (брутто). "
          "Нерозбірливе не вгадуй: залиш порожній рядок і опиши місце в полі notes.")

# М'яка перевірка: латиниця чи кирилиця, цифри, пробіли, «-», «/», «.»; щонайменше 3 цифри.
# Пропускає «CMR-2610-17», «UA 0042517», «АА 123456», «118/26», «№ 0042517».
CMR_NUMBER = re.compile(r"(?:№\s*)?[0-9A-Za-zА-ЯҐЄІЇа-яґєії][0-9A-Za-zА-ЯҐЄІЇа-яґєії\s/.\-]{1,29}")
WEIGHT_TOLERANCE = 0.02       # 2 % на округлення й тару


def looks_like_cmr_number(number: str) -> bool:
    n = " ".join(str(number).split())
    return bool(CMR_NUMBER.fullmatch(n)) and sum(ch.isdigit() for ch in n) >= 3


def check_waybill(wb: Waybill, declared_total_kg: float | None = None, *, today: date | None = None) -> list[str]:
    """Змістові перевірки після схеми: схема гарантує форму, але не правду."""
    issues = []
    if not wb.number.strip():
        issues.append("Номер CMR не прочитано")
    elif not looks_like_cmr_number(wb.number):
        issues.append(f"Підозрілий номер CMR: {wb.number!r}")
    if not wb.date.strip():
        issues.append("Дату не прочитано")
    else:
        try:
            d = date.fromisoformat(wb.date.strip())
        except ValueError:
            issues.append(f"Дата не у форматі РРРР-ММ-ДД: {wb.date!r}")
        else:
            if d > (today or date.today()):
                issues.append(f"Дата з майбутнього: {wb.date}")
    if not wb.items:
        issues.append("Немає жодної вантажної позиції")
    if any(i.weight_kg <= 0 or i.packages < 0 for i in wb.items):
        issues.append("Є позиції з нульовою чи від'ємною вагою або кількістю місць")
    total = sum(i.weight_kg for i in wb.items)
    if declared_total_kg is not None and declared_total_kg > 0 \
            and abs(total - declared_total_kg) > WEIGHT_TOLERANCE * declared_total_kg:
        issues.append(f"Вага {total:g} кг не збігається із заявленою {declared_total_kg:g} кг")
    if any(not f.strip() for f in (wb.sender, wb.consignee, wb.origin, wb.destination)):
        issues.append("Порожні графи сторін або місць – потрібне підтвердження")
    if wb.notes.strip():
        issues.append(f"Модель позначила сумнівні місця: {wb.notes.strip()}")
    return issues


def parse_waybill(resp) -> Waybill | None:
    """Waybill з відповіді: resp.parsed, а якщо його немає – валідація resp.text; інакше None."""
    if isinstance(getattr(resp, "parsed", None), Waybill):
        return resp.parsed
    try:
        text = resp.text
    except (AttributeError, ValueError):
        return None
    if not text:
        return None
    try:
        return Waybill.model_validate_json(text)
    except ValidationError:
        return None


def read_cmr(photo: bytes, declared_total_kg: float | None = None, *, client=None,
             mime_type: str = "image/jpeg", model: str = MODEL_MAIN) -> tuple[Waybill | None, list[str]]:
    """Розбирає фото CMR; повертає (накладна або None, зауваження). Із зауваженнями – людині на перевірку."""
    from .client import make_client
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
    wb = parse_waybill(resp)
    if wb is None:                                 # блок, обрив за MAX_TOKENS, невалідний JSON
        return None, ["Модель не повернула накладну за схемою – потрібен ручний розбір"]
    return wb, check_waybill(wb, declared_total_kg)
