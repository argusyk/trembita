# Додаток Г. Довідник рецептів коду – приклад 40 (рукопис: 93-dodatok-g.md, рядок 816)
import random
import time
import httpx
from google.genai import errors

RETRYABLE = {408, 429, 500, 502, 503, 504}
TRANSIENT = (httpx.TimeoutException, httpx.ConnectError)   # мережа: коду помилки немає

def with_retries(call, attempts: int = 5, base: float = 1.0, cap: float = 30.0):
    for k in range(attempts):
        try:
            return call()
        except (errors.APIError, *TRANSIENT) as e:
            permanent = isinstance(e, errors.APIError) and e.code not in RETRYABLE
            if permanent or k == attempts - 1:
                raise                            # 400, 403, 404 – одразу нагору
            time.sleep(random.random() * min(cap, base * 2 ** k))   # повний джитер
