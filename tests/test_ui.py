from streamlit.testing.v1 import AppTest
from src.valuation import ROOT


def test_offline_and_saved_trial_show_real_provenance_and_verified_numbers():
    app = AppTest.from_file(ROOT / "app.py").run(timeout=30)
    assert not app.exception
    assert any("Replaying" in message.value for message in app.info)
    assert app.metric[3].value == "€955M"
    app.selectbox[1].select("Offline illustration").run(timeout=30)
    assert not app.exception
    assert any("No agents were invoked" in message.value for message in app.info)
    assert not app.button


def test_foundry_requires_explicit_opt_in_and_missing_credentials_fail_visibly(monkeypatch):
    for key in ("FOUNDRY_BASE_URL", "FOUNDRY_MODEL", "FOUNDRY_API_KEY"):
        monkeypatch.delenv(key, raising=False)
    app = AppTest.from_file(ROOT / "app.py").run(timeout=30)
    app.selectbox[1].select("Live Microsoft Foundry").run(timeout=30)
    assert app.button[0].disabled
    app.checkbox[0].check().run(timeout=30)
    app.button[0].click().run(timeout=30)
    assert not app.exception
    assert any("Set Foundry model" in m.value for m in app.markdown)
