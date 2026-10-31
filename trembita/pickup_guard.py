"""Підтвердження людиною для create_pickup (розділ 10)."""
import uuid
from datetime import date as dt_date

SERVICE_CITIES = {"Львів", "Ужгород", "Чернівці", "Київ"}

class PickupGuard:
    def __init__(self, booking_api, audit_log):
        self.pending: dict[str, dict] = {}
        self.booking_api, self.audit = booking_api, audit_log

    def propose(self, address: str, date: str, weight_kg: float) -> dict:
        """Те, що бачить модель: заявка лише готується, нічого не створено."""
        errors = []
        if not any(c in address for c in SERVICE_CITIES):
            errors.append("адреса поза зоною обслуговування")
        if date < date_today():
            errors.append("дата в минулому")
        if not 0 < weight_kg <= 24000:
            errors.append("вага поза межами 0–24000 кг")
        if errors:
            return {"status": "rejected", "errors": errors}
        token = uuid.uuid4().hex[:8]
        self.pending[token] = {"address": address, "date": date, "weight_kg": weight_kg}
        return {"status": "awaiting_human_confirmation", "token": token,
                "message": "Заявку підготовлено. Її має підтвердити диспетчер."}

    def confirm(self, token: str, operator: str) -> dict:
        """Викликає інтерфейс диспетчерської, а не модель."""
        req = self.pending.pop(token)
        result = self.booking_api.create(**req)
        self.audit.write({"action": "create_pickup", "by": operator, **req, "result": result})
        return result

def date_today() -> str:
    return dt_date.today().isoformat()
