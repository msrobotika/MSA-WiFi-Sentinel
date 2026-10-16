from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = "\n".join(
    path.read_text(encoding="utf-8", errors="ignore")
    for path in (ROOT / "firmware" / "src").glob("*.[ch]")
)


def test_no_wifi_frame_transmission_api():
    forbidden = ("esp_wifi_80211_tx", "esp_wifi_internal_tx")
    assert not any(symbol in SOURCE for symbol in forbidden)


def test_status_declares_passive_behavior():
    assert '"passive",true' in SOURCE
    assert '"injection_enabled",false' in SOURCE
    assert '"wifi_connected",false' in SOURCE


def test_no_password_storage_contract():
    lowered = SOURCE.lower()
    assert "wifi_password" not in lowered
    assert "passphrase" not in lowered
