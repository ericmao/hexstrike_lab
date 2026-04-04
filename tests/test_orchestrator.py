from pathlib import Path
from unittest.mock import patch

from hexstrike_lab.core.config import load_config
from hexstrike_lab.core.schema import validate_scan_document
from hexstrike_lab.execution.base import ToolResult
from hexstrike_lab.execution.orchestrator import ExecutionOrchestrator


def test_merge_into_report_includes_evidence_record():
    root = Path(__file__).resolve().parents[1]
    cfg = load_config(root / "configs" / "default.yaml")
    orch = ExecutionOrchestrator()
    profile = {
        "name": "quick",
        "steps": [{"adapter": "nmap", "timeout_sec": 10, "retries": 0, "options": {"ports": "443"}}],
    }
    orchestration = orch.run_profile(target="192.0.2.1", profile=profile, dry_run=True)
    doc = orch.merge_into_report(cfg, orchestration, "192.0.2.1")
    assert doc["findings"][0]["evidence_record"]["schema"] == "hexstrike.pentest_evidence.v1"
    validate_scan_document(doc)


def test_dry_run_quick_profile():
    orch = ExecutionOrchestrator()
    profile = {
        "name": "quick",
        "steps": [
            {"adapter": "nmap", "timeout_sec": 60, "retries": 0, "options": {"ports": "443"}},
        ],
    }
    out = orch.run_profile(target="192.0.2.1", profile=profile, dry_run=True)
    assert out["dry_run"] is True
    assert len(out["steps"]) == 1
    assert out["steps"][0]["status"] == "planned"
    assert "nmap" in out["steps"][0]["command"][0]


def test_dry_run_adaptive_web_plans_both_steps():
    orch = ExecutionOrchestrator()
    profile = {
        "name": "adaptive_web",
        "steps": [
            {"adapter": "nmap", "timeout_sec": 10, "retries": 0, "options": {"ports": "80"}},
            {
                "adapter": "nikto",
                "run_when": {"after_adapter": "nmap", "open_ports_any_of": [80]},
                "timeout_sec": 10,
                "retries": 0,
                "options": {"ssl": False, "port": 80, "maxtime_sec": 1},
            },
        ],
    }
    out = orch.run_profile(target="192.0.2.1", profile=profile, dry_run=True)
    assert len(out["steps"]) == 2
    assert out["steps"][0]["status"] == "planned"
    assert out["steps"][1]["status"] == "planned"


def test_adaptive_skip_nikto_when_no_web_port():
    orch = ExecutionOrchestrator()
    profile = {
        "name": "adaptive_web",
        "steps": [
            {"adapter": "nmap", "timeout_sec": 10, "retries": 0, "options": {"ports": "22"}},
            {
                "adapter": "nikto",
                "run_when": {"after_adapter": "nmap", "open_ports_any_of": [80, 443]},
                "timeout_sec": 10,
                "retries": 0,
                "options": {"ssl": True, "port": 443, "maxtime_sec": 1},
            },
        ],
    }

    def _fake_run(adapter, target, **kwargs):
        if adapter.name == "nmap":
            return ToolResult(
                adapter="nmap",
                target=target,
                status="ok",
                exit_code=0,
                duration_ms=1.0,
                stdout="",
                stderr="",
                command=["nmap"],
                parsed={
                    "data": {
                        "open_ports": [
                            {"port": 22, "protocol": "tcp", "service": "ssh", "detail": ""},
                        ]
                    }
                },
            )
        raise AssertionError("nikto should not run when condition fails")

    with patch("hexstrike_lab.execution.orchestrator.run_adapter", side_effect=_fake_run):
        out = orch.run_profile(target="192.0.2.1", profile=profile, dry_run=False)

    assert len(out["steps"]) == 2
    assert out["steps"][0]["status"] == "ok"
    assert out["steps"][1]["status"] == "skipped"


def test_adaptive_runs_nikto_when_web_port_open():
    orch = ExecutionOrchestrator()
    profile = {
        "name": "adaptive_web",
        "steps": [
            {"adapter": "nmap", "timeout_sec": 10, "retries": 0, "options": {"ports": "443"}},
            {
                "adapter": "nikto",
                "run_when": {"after_adapter": "nmap", "open_ports_any_of": [443]},
                "timeout_sec": 10,
                "retries": 0,
                "options": {"ssl": True, "port": 443, "maxtime_sec": 1},
            },
        ],
    }
    calls: list[str] = []

    def _fake_run(adapter, target, **kwargs):
        calls.append(adapter.name)
        if adapter.name == "nmap":
            return ToolResult(
                adapter="nmap",
                target=target,
                status="ok",
                exit_code=0,
                duration_ms=1.0,
                stdout="",
                stderr="",
                command=["nmap"],
                parsed={
                    "data": {
                        "open_ports": [
                            {"port": 443, "protocol": "tcp", "service": "https", "detail": ""},
                        ]
                    }
                },
            )
        return ToolResult(
            adapter="nikto",
            target=target,
            status="ok",
            exit_code=0,
            duration_ms=1.0,
            stdout="+ done\n",
            stderr="",
            command=["nikto"],
            parsed={"data": {"findings": [], "finding_count": 0, "truncated": False}},
        )

    with patch("hexstrike_lab.execution.orchestrator.run_adapter", side_effect=_fake_run):
        out = orch.run_profile(target="192.0.2.1", profile=profile, dry_run=False)

    assert calls == ["nmap", "nikto"]
    assert out["steps"][1]["status"] == "ok"
