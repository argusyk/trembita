"""Підтвердження людиною для create_pickup (розділ 10): модель пропонує, людина підтверджує, код виконує.

Модель бачить лише propose() (під назвою create_pickup): вона перевіряє аргументи і ставить заявку
в чергу. Справжнє створення – лише confirm(), яку викликає інтерфейс диспетчерської, а не модель.
"""
import re
import secrets
import time
import zlib
import datetime as dt

from . import data

MAX_PICKUP_KG = 24_000            # вантажопідйомність тягача з напівпричепом – одна межа для всієї книги
TOKEN_TTL_S = 30 * 60             # непідтверджена заявка «згорає» через 30 хвилин
SERVICE_CITIES = frozenset(data.WAREHOUSES)   # зона обслуговування – міста зі складами «Смереки»

_CITY_PREFIX = re.compile(r"^(?:м\.|місто\s)\s*", re.IGNORECASE)


def normalize_city(name: str) -> str:
    """«м. Львів» / «ЛЬВІВ » / «місто Львів» -> «львів»."""
    name = " ".join(str(name).split())
    return _CITY_PREFIX.sub("", name).strip().casefold()


def city_of(address: str) -> str | None:
    """Місто з адреси формату «м. Львів, вул. Зелена, 1» (перший елемент) або None, якщо поза зоною.

    Перевірка точна: «Одеса, вул. Київська, 5» не потрапляє в зону через слово «Київська».
    """
    first = str(address).split(",", 1)[0]
    city = normalize_city(first)
    return city if city in SERVICE_CITIES else None


def validate_pickup(address: str, date_str: str, weight_kg, *, today: dt.date | None = None) -> list[str]:
    """Перевіряє аргументи заявки; повертає список помилок (порожній – усе гаразд)."""
    errors = []
    if city_of(address) is None:
        errors.append("адреса поза зоною обслуговування (формат: «м. Львів, вул. ..., буд.»; "
                      f"міста: {', '.join(sorted(c.capitalize() for c in SERVICE_CITIES))})")
    try:
        day = dt.date.fromisoformat(str(date_str))
    except ValueError:
        errors.append("дата має бути у форматі РРРР-ММ-ДД")
    else:
        if day < (today or dt.date.today()):
            errors.append("дата в минулому")
    try:
        w = float(weight_kg)
    except (TypeError, ValueError):
        errors.append("вага має бути числом")
    else:
        if not 0 < w <= MAX_PICKUP_KG:
            errors.append(f"вага поза межами 0–{MAX_PICKUP_KG} кг")
    return errors


class DemoBookingAPI:
    """Імітація системи заявок «Смереки»: детермінований номер, повтор із тим самим ключем – той самий результат."""

    def __init__(self):
        self.created: dict[str, dict] = {}

    def create(self, address: str, date: str, weight_kg: float, idempotency_key: str) -> dict:
        if idempotency_key in self.created:                # ключ ідемпотентності: без дублікатів
            return self.created[idempotency_key]
        day = dt.date.fromisoformat(date)
        pickup_id = f"PU-{day:%m%d}-{zlib.crc32(address.encode()) % 10000:04d}"
        result = {"status": "створено", "pickup_id": pickup_id, "address": address,
                  "date": day.isoformat(), "weight_kg": weight_kg}
        self.created[idempotency_key] = result
        return result


class ListAudit:
    """Найпростіший журнал аудиту: список записів у пам'яті."""

    def __init__(self):
        self.records: list[dict] = []

    def write(self, record: dict) -> None:
        self.records.append(record)


class PickupGuard:
    def __init__(self, booking_api, audit_log, *, ttl_s: float = TOKEN_TTL_S,
                 clock=time.time, today=dt.date.today):
        self.pending: dict[str, dict] = {}
        self.booking_api, self.audit = booking_api, audit_log
        self.ttl_s, self.clock, self.today = ttl_s, clock, today

    def propose(self, address: str, date: str, weight_kg: float) -> dict:
        """Те, що бачить модель: заявка лише готується, нічого не створено."""
        errors = validate_pickup(address, date, weight_kg, today=self.today())
        if errors:
            self.audit.write({"action": "propose_pickup", "address": address, "date": date,
                              "weight_kg": weight_kg, "result": "rejected", "errors": errors})
            return {"status": "rejected", "errors": errors}
        token = secrets.token_hex(8)                       # не вгадати й не перебрати
        req = {"address": " ".join(str(address).split()),
               "date": dt.date.fromisoformat(str(date)).isoformat(), "weight_kg": float(weight_kg)}
        self.pending[token] = {**req, "expires_at": self.clock() + self.ttl_s}
        self.audit.write({"action": "propose_pickup", **req, "token": token, "result": "pending"})
        return {"status": "awaiting_human_confirmation", "token": token,
                "message": "Заявку підготовлено. Її має підтвердити диспетчер."}

    def confirm(self, token: str, operator: str) -> dict:
        """Викликає інтерфейс диспетчерської, а не модель."""
        entry = self.pending.pop(token, None)              # pop: повторне підтвердження не створить дубль
        if entry is None:
            return {"status": "error", "error": "невідома або вже оброблена заявка"}
        expires_at = entry.pop("expires_at")
        if self.clock() > expires_at:
            self.audit.write({"action": "create_pickup", "by": operator, **entry, "result": "expired"})
            return {"status": "error", "error": "термін підтвердження минув – підготуйте заявку знову"}
        errors = validate_pickup(entry["address"], entry["date"], entry["weight_kg"], today=self.today())
        if errors:                                         # напр., дата стала минулою, поки чекали
            self.audit.write({"action": "create_pickup", "by": operator, **entry,
                              "result": "rejected", "errors": errors})
            return {"status": "rejected", "errors": errors}
        result = self.booking_api.create(**entry, idempotency_key=token)
        self.audit.write({"action": "create_pickup", "by": operator, **entry, "result": result})
        return result

    def reject(self, token: str, operator: str, reason: str = "") -> dict:
        """Диспетчер відхиляє заявку."""
        entry = self.pending.pop(token, None)
        if entry is None:
            return {"status": "error", "error": "невідома або вже оброблена заявка"}
        entry.pop("expires_at")
        self.audit.write({"action": "create_pickup", "by": operator, **entry,
                          "result": "rejected_by_operator", "reason": reason})
        return {"status": "rejected", "errors": [reason or "диспетчер відхилив заявку"]}

    def as_tool(self):
        """Функція create_pickup для моделі, прив'язана до цього охоронця (для AFC/ADK/ручного циклу)."""
        def create_pickup(address: str, date: str, weight_kg: float) -> dict:
            """Готує заявку на забір вантажу. Заявку створює лише диспетчер після підтвердження.

            Args:
                address: адреса забору у форматі «м. Львів, вул. Зелена, 1» (місто – першим).
                date: дата забору РРРР-ММ-ДД, не раніше сьогодні.
                weight_kg: вага брутто, кг (до 24000).
            """
            return self.propose(address, date, weight_kg)
        return create_pickup


_default: "PickupGuard | None" = None


def default_guard() -> PickupGuard:
    """Спільний охоронець процесу з демонстраційним API заявок і журналом у пам'яті."""
    global _default
    if _default is None:
        _default = PickupGuard(DemoBookingAPI(), ListAudit())
    return _default
