"""Інструменти «Трембіти» для виклику функцій (розділ 10).

Сигнатури й докстрінги – це те, що бачить модель: SDK (і ADK) будує з них оголошення функцій.
Функції читання повертають словник; помилку – як {"error": ...}, а не виняток, щоб модель могла
попросити клієнта уточнити дані. Дія з наслідками create_pickup нічого не створює сама: вона лише
ставить заявку в чергу PickupGuard, а створює її диспетчер (pickup_guard.PickupGuard.confirm).
"""
import re

from . import data
from .pickup_guard import default_guard, normalize_city

SHIPMENT_ID = re.compile(r"^SM-\d{4}-\d{4}$")


def track_shipment(shipment_id: str) -> dict:
    """Повертає статус, місцезнаходження й очікувану дату прибуття відправлення.

    Args:
        shipment_id: номер відправлення виду SM-2610-0042.
    """
    sid = str(shipment_id).strip().upper()
    if not SHIPMENT_ID.match(sid):
        return {"error": f"номер {shipment_id!r} не схожий на номер відправлення SM-РРММ-NNNN"}
    rec = data.SHIPMENTS.get(sid)
    if rec is None:
        return {"error": f"відправлення {sid} не знайдено"}
    return {"shipment_id": sid, **rec}


def chargeable_weight(weight_kg: float, volume_m3: float = 0.0) -> float:
    """Платна вага: більша з фактичної та об'ємної (250 кг на 1 м³)."""
    return max(weight_kg, volume_m3 * data.VOLUME_FACTOR)


def get_tariff(origin: str, destination: str, weight_kg: float, volume_m3: float = 0.0) -> dict:
    """Розраховує вартість перевезення між містами (грн, без ПДВ). Викликай, коли клієнт питає ціну доставки.

    Args:
        origin: місто відправлення, напр. «Львів».
        destination: місто призначення.
        weight_kg: вага брутто, кг.
        volume_m3: об'єм вантажу, м³ (0, якщо невідомий).
    """
    try:
        weight_kg, volume_m3 = float(weight_kg), float(volume_m3 or 0.0)
    except (TypeError, ValueError):
        return {"error": "вага й об'єм мають бути числами"}
    if weight_kg <= 0 or volume_m3 < 0:
        return {"error": "вага має бути додатною, об'єм – невід'ємним"}
    rate = data.BASE_RATE.get((normalize_city(origin), normalize_city(destination)))
    if rate is None:
        return {"error": f"напрямок {origin} – {destination} не обслуговується"}
    w = chargeable_weight(weight_kg, volume_m3)
    return {"origin": origin, "destination": destination, "chargeable_kg": round(w, 1),
            "price_uah": round(max(data.MIN_CHARGE, w * rate), 2)}


def find_warehouse(city: str) -> dict:
    """Повертає адресу й години роботи складу «Смереки» в місті.

    Args:
        city: назва міста, напр. «Ужгород».
    """
    wh = data.WAREHOUSES.get(normalize_city(city))
    return {"city": city, **wh} if wh else {"error": f"у місті {city} складу «Смереки» немає"}


def create_pickup(address: str, date: str, weight_kg: float) -> dict:
    """Готує заявку на забір вантажу. Сама заявку не створює: її підтверджує диспетчер.

    Args:
        address: адреса забору у форматі «м. Львів, вул. Зелена, 1» (місто – першим).
        date: дата забору РРРР-ММ-ДД, не раніше сьогодні.
        weight_kg: вага брутто, кг (до 24000).
    """
    return default_guard().propose(address, date, weight_kg)


READ_ONLY = [track_shipment, get_tariff, find_warehouse]   # для AFC у клієнтському чаті
WITH_EFFECTS = {"create_pickup"}                            # лише через PickupGuard і людину
