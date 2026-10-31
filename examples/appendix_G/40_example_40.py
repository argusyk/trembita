# Додаток Г. Довідник рецептів коду – приклад 40 (рукопис: 93-dodatok-g.md, рядок 800)
import random
import time
from google.genai import errors

RETRYABLE = {429, 500, 503, 504}

def with_retries(call, attempts: int = 5, base: float = 1.0, cap: float = 30.0):
    for k in range(attempts):
        try:
            return call()
        except errors.APIError as e:
            if e.code not in RETRYABLE or k == attempts - 1:
                raise                            # 400, 403, 404 – одразу нагору
            time.sleep(random.random() * min(cap, base * 2 ** k))   # повний джитер
