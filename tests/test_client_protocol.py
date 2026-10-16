import importlib.util
from pathlib import Path


PATH = Path(__file__).resolve().parents[1] / "tools" / "device.py"
SPEC = importlib.util.spec_from_file_location("device", PATH)
DEVICE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(DEVICE)


def test_cli_requires_explicit_owner_confirmation():
    parser_source = PATH.read_text(encoding="utf-8")
    assert "--confirm-owned-network" in parser_source
    assert "required=True" in parser_source


def test_ap_record_limit_is_bounded():
    assert "while len(out)<64" in PATH.read_text(encoding="utf-8")
