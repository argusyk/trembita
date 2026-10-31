import pytest
from google.genai import errors

from trembita import client


def test_backoff_bounded():
    d = client.backoff_delays(6, base=1, cap=8, rng=lambda: 1.0)
    assert d == [1, 2, 4, 8, 8]


def test_retries_on_429_then_succeeds():
    attempts = []
    def call():
        attempts.append(1)
        if len(attempts) < 3:
            raise errors.ClientError(429, {"error": {"message": "quota", "status": "RESOURCE_EXHAUSTED"}})
        return "ok"
    assert client.with_retries(call, sleep=lambda s: None) == "ok" and len(attempts) == 3


def test_no_retry_on_400():
    def call():
        raise errors.ClientError(400, {"error": {"message": "bad", "status": "INVALID_ARGUMENT"}})
    with pytest.raises(errors.ClientError):
        client.with_retries(call, sleep=lambda s: None)
