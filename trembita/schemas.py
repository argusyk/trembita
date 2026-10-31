"""Pydantic-схеми для структурованих відповідей (розділ 11)."""
from enum import Enum

from pydantic import BaseModel, Field


class CargoItem(BaseModel):
    name: str = Field(description="Найменування вантажу")
    packages: int = Field(ge=0, description="Кількість місць")
    weight_kg: float = Field(ge=0, description="Вага брутто, кг")


class Waybill(BaseModel):
    """Міжнародна товарно-транспортна накладна CMR."""
    number: str
    date: str = Field(description="Дата складання, РРРР-ММ-ДД")
    sender: str
    consignee: str
    origin: str
    destination: str
    items: list[CargoItem]


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
