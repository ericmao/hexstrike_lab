import pytest

from hexstrike_lab.execution.conditions import evaluate_run_when


def test_evaluate_run_when_missing_always_runs():
    ok, reason = evaluate_run_when(None, [], dry_run=False)
    assert ok and reason is None
    ok, reason = evaluate_run_when({}, [], dry_run=False)
    assert ok and reason is None


def test_evaluate_run_when_dry_run_ignores_prior_steps():
    rw = {"after_adapter": "nmap", "open_ports_any_of": [80]}
    ok, _ = evaluate_run_when(rw, [], dry_run=True)
    assert ok


def test_evaluate_run_when_requires_prior_ok_nmap_with_ports():
    rw = {"after_adapter": "nmap", "open_ports_any_of": [443]}
    prior = [
        {
            "adapter": "nmap",
            "status": "ok",
            "parsed": {"data": {"open_ports": [{"port": 22, "protocol": "tcp", "service": "ssh", "detail": ""}]}},
        }
    ]
    ok, reason = evaluate_run_when(rw, prior, dry_run=False)
    assert not ok
    assert reason is not None
    assert "443" in reason or "no open port" in reason

    prior[0]["parsed"]["data"]["open_ports"].append(
        {"port": 443, "protocol": "tcp", "service": "https", "detail": ""}
    )
    ok, reason = evaluate_run_when(rw, prior, dry_run=False)
    assert ok and reason is None


def test_evaluate_run_when_fails_if_prior_not_ok():
    rw = {"after_adapter": "nmap", "open_ports_any_of": [80]}
    prior = [{"adapter": "nmap", "status": "error", "parsed": {"data": {"open_ports": []}}}]
    ok, reason = evaluate_run_when(rw, prior, dry_run=False)
    assert not ok
    assert "need ok" in (reason or "").lower()


def test_evaluate_run_when_invalid_shape():
    with pytest.raises(ValueError, match="mapping"):
        evaluate_run_when("always", [], dry_run=False)
    with pytest.raises(ValueError, match="after_adapter"):
        evaluate_run_when({"after_adapter": "nmap"}, [], dry_run=False)
