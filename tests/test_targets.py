import pytest

from hexstrike_lab.execution.targets import validate_lab_target


def test_accepts_ipv4():
    assert validate_lab_target("192.0.2.1") == "192.0.2.1"


def test_rejects_shell_chars():
    with pytest.raises(ValueError):
        validate_lab_target("127.0.0.1;rm -rf /")
