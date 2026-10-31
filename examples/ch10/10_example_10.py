# Розділ 10. Виклик функцій – приклад 10 (рукопис: 10-funktsii.md, рядок 426)
class PickupGuard:                    # продовження trembita/pickup_guard.py
    def __init__(self, booking_api, audit_log, *, ttl_s: float = TOKEN_TTL_S,
                 clock=time.time, today=dt.date.today):
        self.pending: dict[str, dict] = {}
        self.booking_api, self.audit = booking_api, audit_log
        self.ttl_s, self.clock, self.today = ttl_s, clock, today

    def propose(self, address: str, date: str, weight_kg: float) -> dict:
        """Те, що бачить модель: заявка лише готується, нічого не створено."""
        errors = validate_pickup(address, date, weight_kg, today=self.today())
        if errors:
            ...                                        # запис у журнал аудиту
            return {"status": "rejected", "errors": errors}
        token = secrets.token_hex(8)                   # не вгадати й не перебрати
        req = {"address": " ".join(str(address).split()),
               "date": dt.date.fromisoformat(str(date)).isoformat(), "weight_kg": float(weight_kg)}
        self.pending[token] = {**req, "expires_at": self.clock() + self.ttl_s}
        ...                                            # запис у журнал аудиту
        return {"status": "awaiting_human_confirmation", "token": token,
                "message": "Заявку підготовлено. Її має підтвердити диспетчер."}

    def confirm(self, token: str, operator: str) -> dict:
        """Викликає інтерфейс диспетчерської, а не модель."""
        entry = self.pending.pop(token, None)          # pop: повторне підтвердження не створить дубль
        if entry is None:
            return {"status": "error", "error": "невідома або вже оброблена заявка"}
        if self.clock() > entry.pop("expires_at"):
            ...                                        # запис у журнал: термін минув
            return {"status": "error", "error": "термін підтвердження минув – підготуйте заявку знову"}
        errors = validate_pickup(entry["address"], entry["date"], entry["weight_kg"], today=self.today())
        if errors:                                     # напр., дата стала минулою, поки чекали
            ...
            return {"status": "rejected", "errors": errors}
        result = self.booking_api.create(**entry, idempotency_key=token)
        self.audit.write({"action": "create_pickup", "by": operator, **entry, "result": result})
        return result
