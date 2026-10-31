# Додаток Г. Довідник рецептів коду – приклад 4 (рукопис: 93-dodatok-g.md, рядок 57)
retry = types.HttpRetryOptions(
    attempts=3,                      # разом із першою спробою
    initial_delay=1.0, max_delay=8.0, exp_base=2.0, jitter=1.0,   # секунди
    http_status_codes=[408, 429, 500, 502, 503, 504],
)
client = genai.Client(
    http_options=types.HttpOptions(timeout=20_000, retry_options=retry),  # мілісекунди
)
