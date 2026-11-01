# Chapter 10. Function Calling – example 10 (manuscript: 10-funktsii.md, line 426)
class PickupGuard:                    # continuation of trembita/pickup_guard.py
    def __init__(self, booking_api, audit_log, *, ttl_s: float = TOKEN_TTL_S,
                 clock=time.time, today=dt.date.today):
        self.pending: dict[str, dict] = {}
        self.booking_api, self.audit = booking_api, audit_log
        self.ttl_s, self.clock, self.today = ttl_s, clock, today

    def propose(self, address: str, date: str, weight_kg: float) -> dict:
        """What the model sees: the request is only being prepared, nothing is created."""
        errors = validate_pickup(address, date, weight_kg, today=self.today())
        if errors:
            ...                                        # audit log entry
            return {"status": "rejected", "errors": errors}
        token = secrets.token_hex(8)                   # cannot be guessed or brute-forced
        req = {"address": " ".join(str(address).split()),
               "date": dt.date.fromisoformat(str(date)).isoformat(), "weight_kg": float(weight_kg)}
        self.pending[token] = {**req, "expires_at": self.clock() + self.ttl_s}
        ...                                            # audit log entry
        return {"status": "awaiting_human_confirmation", "token": token,
                "message": "The request has been prepared. A dispatcher must confirm it."}

    def confirm(self, token: str, operator: str) -> dict:
        """Called by the dispatch office interface, not by the model."""
        entry = self.pending.pop(token, None)          # pop: a repeated confirmation creates no duplicate
        if entry is None:
            return {"status": "error", "error": "unknown or already processed request"}
        if self.clock() > entry.pop("expires_at"):
            ...                                        # log entry: expired
            return {"status": "error", "error": "confirmation period expired – prepare the request again"}
        errors = validate_pickup(entry["address"], entry["date"], entry["weight_kg"], today=self.today())
        if errors:                                     # e.g. the date became past while waiting
            ...
            return {"status": "rejected", "errors": errors}
        result = self.booking_api.create(**entry, idempotency_key=token)
        self.audit.write({"action": "create_pickup", "by": operator, **entry, "result": result})
        return result
