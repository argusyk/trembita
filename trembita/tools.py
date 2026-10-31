"""Інструменти «Трембіти» для виклику функцій (розділ 10).

Сигнатури й докстрінги – це те, що бачить модель: SDK будує з них оголошення функцій.
"""
import zlib
from datetime import date as _date

from . import data


def track_shipment(shipment_id: str) -> dict:
    """Повертає статус і місцезнаходження відправлення за номером виду SM-2610-0042."""
    rec = data.SHIPMENTS.get(shipment_id.strip().upper())
    if rec is None:
        return {"error": f"відправлення {shipment_id} не знайдено"}
    return {"shipment_id": shipment_id.upper(), **rec}


def chargeable_weight(weight_kg: float, volume_m3: float = 0.0) -> float:
    """Платна вага: більша з фактичної та об'ємної."""
    return max(weight_kg, volume_m3 * data.VOLUME_FACTOR)


def get_tariff(origin: str, destination: str, weight_kg: float, volume_m3: float = 0.0) -> dict:
    """Розраховує вартість доставки між містами за вагою (кг) і об'ємом (м³)."""
    if weight_kg <= 0 or volume_m3 < 0:
        return {"error": "вага має бути додатною, об'єм – невід'ємним"}
    rate = data.BASE_RATE.get((origin.strip().lower(), destination.strip().lower()))
    if rate is None:
        return {"error": f"напрямок {origin} – {destination} не обслуговується"}
    w = chargeable_weight(weight_kg, volume_m3)
    return {"origin": origin, "destination": destination, "chargeable_kg": round(w, 1),
            "price_uah": round(max(data.MIN_CHARGE, w * rate), 2)}


def find_warehouse(city: str) -> dict:
    """Повертає адресу й години роботи складу «Смереки» в місті."""
    wh = data.WAREHOUSES.get(city.strip().lower())
    return {"city": city, **wh} if wh else {"error": f"у місті {city} складу немає"}


def create_pickup(address: str, date: str, weight_kg: float) -> dict:
    """Створює заявку на забір вантажу. Дія з наслідками: викликати лише після підтвердження."""
    try:
        day = _date.fromisoformat(date)
    except ValueError:
        return {"error": "дата має бути у форматі РРРР-ММ-ДД"}
    if weight_kg <= 0:
        return {"error": "вага має бути додатною"}
    return {"pickup_id": f"PU-{day:%m%d}-{zlib.crc32(address.encode()) % 10000:04d}", "address": address,
            "date": day.isoformat(), "weight_kg": weight_kg, "status": "створено"}


READ_ONLY = [track_shipment, get_tariff, find_warehouse]
WITH_EFFECTS = {"create_pickup"}
