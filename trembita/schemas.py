"""Pydantic-схеми для структурованих відповідей (розділ 11).

Описи полів потрапляють у схему, і модель читає їх як інструкцію (звідки брати вагу тощо).
Обмежень на кшталт ge=0 тут свідомо немає: невалідне значення зробило б resp.parsed порожнім,
а змістові перевірки (documents.check_waybill) повідомляють про проблему зрозуміло.
"""
from enum import Enum

from pydantic import BaseModel, Field


class CargoItem(BaseModel):
    name: str = Field(description="Найменування вантажу (графа 9 CMR)")
    packages: int = Field(description="Кількість місць (графа 7)")
    weight_kg: float = Field(description="Вага брутто в кг (графа 11)")


class Waybill(BaseModel):
    """Міжнародна товарно-транспортна накладна CMR."""
    number: str = Field(description="Номер накладної CMR")
    date: str = Field(description="Дата складання у форматі РРРР-ММ-ДД")
    sender: str = Field(description="Відправник (графа 1)")
    consignee: str = Field(description="Одержувач (графа 2)")
    origin: str = Field(description="Місце завантаження (графа 4)")
    destination: str = Field(description="Місце розвантаження (графа 3)")
    items: list[CargoItem] = Field(description="Вантажні позиції")
    notes: str = Field(default="", description="Нерозбірливі чи сумнівні місця бланка; порожньо, якщо таких немає")


class ClaimCategory(str, Enum):
    damage = "пошкодження"
    delay = "затримка"
    loss = "втрата"
    billing = "рахунок"
    other = "інше"


class ClaimTriage(BaseModel):
    category: ClaimCategory
    shipment_id: str | None = None
    urgent: bool
    summary: str = Field(description="Суть претензії одним реченням")
