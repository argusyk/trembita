# Appendix D. Code Recipes – example 40 (manuscript: 93-appendix-d.md, line 816)
import random
import time
import httpx
from google.genai import errors

RETRYABLE = {408, 429, 500, 502, 503, 504}
TRANSIENT = (httpx.TimeoutException, httpx.ConnectError)   # network: there is no error code

def with_retries(call, attempts: int = 5, base: float = 1.0, cap: float = 30.0):
    for k in range(attempts):
        try:
            return call()
        except (errors.APIError, *TRANSIENT) as e:
            permanent = isinstance(e, errors.APIError) and e.code not in RETRYABLE
            if permanent or k == attempts - 1:
                raise                            # 400, 403, 404 – straight up the stack
            time.sleep(random.random() * min(cap, base * 2 ** k))   # full jitter
