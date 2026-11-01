# Appendix D. Code Recipes – example 4 (manuscript: 93-appendix-d.md, line 57)
retry = types.HttpRetryOptions(
    attempts=3,                      # including the first attempt
    initial_delay=1.0, max_delay=8.0, exp_base=2.0, jitter=1.0,   # seconds
    http_status_codes=[408, 429, 500, 502, 503, 504],
)
client = genai.Client(
    http_options=types.HttpOptions(timeout=20_000, retry_options=retry),  # milliseconds
)
