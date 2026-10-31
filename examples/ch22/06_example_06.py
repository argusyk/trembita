# Розділ 22. Комп'ютерне використання та браузерні агенти – приклад 6 (рукопис: 22-computer-use.md, рядок 287)
from urllib.parse import urlparse

ALLOWED_HOSTS = {"portal.customs.example", "static.customs.example"}


def guard(route):
    """Пропускає лише запити до дозволених доменів, решту обриває."""
    host = urlparse(route.request.url).hostname or ""
    if host in ALLOWED_HOSTS:
        route.continue_()
    else:
        route.abort()

# context.route("**/*", guard)  – для всього контексту браузера
