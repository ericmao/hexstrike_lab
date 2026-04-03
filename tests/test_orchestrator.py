from hexstrike_lab.execution.orchestrator import ExecutionOrchestrator


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
