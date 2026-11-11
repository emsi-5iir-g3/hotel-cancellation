import httpx
import pytest
from streamlit.testing.v1 import AppTest

from maintai.client import APIError, MaintaiClient
from test_ui import APP


@pytest.mark.parametrize("error, expected", [
    (APIError(401, "Clé API invalide"), "Erreur 401"),
    (httpx.ConnectError("Connexion refusée"), "API injoignable"),
])
def test_ui_reports_errors(settings_env, monkeypatch, error, expected):
    def refuse(self, reading):
        raise error

    monkeypatch.setattr(MaintaiClient, "predict", refuse)
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.button[0].click().run()
    assert not at.exception
    messages = [item.value for item in at.warning] + [item.value for item in at.error]
    assert any(expected in message for message in messages)


def test_ui_reports_normal_prediction(settings_env, monkeypatch):
    monkeypatch.setattr(MaintaiClient, "predict", lambda self, reading: {
        "failure_probability": 0.05, "alert": False,
        "threshold": 0.3, "model_version": "test",
    })
    at = AppTest.from_file(APP, default_timeout=30).run()
    at.button[0].click().run()
    assert not at.exception
    assert at.metric[-1].value == "5 %"
    assert "Normal" in at.success[0].value
