import importlib

import pytest

from trembita import config


def test_defaults_and_new_models():
    assert config.MODEL_FALLBACK == "gemini-3.5-flash"
    assert config.MODEL_IMAGE and config.MODEL_TTS
    assert config.MODEL_MAIN in config.PRICES and config.MODEL_SMART in config.PRICES


def test_env_override_and_latest_forbidden(monkeypatch):
    try:
        monkeypatch.setenv("TREMBITA_MODEL_SMART", "gemini-3.8-flash")
        assert importlib.reload(config).MODEL_SMART == "gemini-3.8-flash"
        monkeypatch.setenv("TREMBITA_MODEL", "gemini-flash-latest")
        with pytest.raises(ValueError, match="latest"):
            importlib.reload(config)
    finally:
        monkeypatch.delenv("TREMBITA_MODEL", raising=False)
        monkeypatch.delenv("TREMBITA_MODEL_SMART", raising=False)
        importlib.reload(config)
