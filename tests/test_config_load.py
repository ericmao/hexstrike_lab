from pathlib import Path

from hexstrike_lab.core.config import load_config


def test_load_default_yaml():
    root = Path(__file__).resolve().parents[1]
    cfg = load_config(root / "configs" / "default.yaml")
    assert cfg["lab"]["name"] == "hexstrike_lab"
    assert "logging" in cfg
