# Chapter 22. Computer Use and Browser Agents – example 7 (manuscript: 22-computer-use.md, line 327)
from urllib.parse import urlparse

ALLOWED_HOSTS = {"portal.customs.example", "static.customs.example"}


def guard(route):
    """Lets through only requests to allowed domains, aborts the rest."""
    host = urlparse(route.request.url).hostname or ""
    if host in ALLOWED_HOSTS:
        route.continue_()
    else:
        route.abort()

# context.route("**/*", guard)  – for the whole browser context
