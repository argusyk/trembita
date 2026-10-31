# Розділ 23. Промислова експлуатація на Gemini Enterprise Agent Platform – приклад 3 (рукопис: 23-produkshn.md, рядок 189)
import time
from google import genai
from google.genai import errors
from trembita.config import MODEL_MAIN, MODEL_LITE


class CircuitBreaker:
    def __init__(self, threshold: int = 5, cooldown: float = 30.0):
        self.threshold, self.cooldown = threshold, cooldown
        self.failures, self.opened_at = 0, None

    def allow(self) -> bool:
        if self.opened_at is None:
            return True                                            # замкнено
        return time.monotonic() - self.opened_at >= self.cooldown  # напіввідкрито: пробний запит

    def record(self, ok: bool) -> None:
        if ok:
            self.failures, self.opened_at = 0, None                # знову замкнено
        else:
            self.failures += 1
            if self.failures >= self.threshold:
                self.opened_at = time.monotonic()                  # розімкнено на паузу


CHAIN = [MODEL_MAIN, "gemini-3.5-flash", MODEL_LITE]
BREAKERS = {m: CircuitBreaker() for m in CHAIN}


def ask_with_fallback(client: genai.Client, question: str) -> str:
    for model in CHAIN:
        if not BREAKERS[model].allow():
            continue
        try:
            resp = client.models.generate_content(model=model, contents=question)
        except errors.ServerError:
            BREAKERS[model].record(False); continue
        except errors.ClientError as e:
            if e.code != 429:
                raise            # 400/403/404 – помилка в нашому запиті, резерв не допоможе
            BREAKERS[model].record(False); continue
        BREAKERS[model].record(True)
        return resp.text
    return "Зараз «Трембіта» перевантажена. Диспетчер відповість вам особисто."
