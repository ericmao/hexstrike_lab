from hexstrike_lab.core.evidence_schema import build_evidence_record, validate_evidence_record


def test_build_evidence_record_minimal_ok():
    step = {
        "adapter": "nmap",
        "status": "planned",
        "target": "192.0.2.1",
        "command": ["nmap", "192.0.2.1"],
    }
    rec = build_evidence_record(step, step_index=0, target_host="192.0.2.1")
    assert rec["schema"] == "hexstrike.pentest_evidence.v1"
    assert rec["execution_status"] == "planned"
    validate_evidence_record(rec)


def test_build_evidence_record_with_lab_metadata():
    step = {
        "adapter": "nikto",
        "status": "ok",
        "command": ["nikto", "-h", "https://x/"],
        "exit_code": 0,
        "duration_ms": 10.0,
        "collected_at": "2026-04-04T12:00:00+00:00",
        "pentest_phase": "web_assessment",
        "workflow_step_id": "PT-WEB-01",
        "objective": "Web checks",
        "parsed": {"data": {"finding_count": 3, "open_count": 0}},
    }
    rec = build_evidence_record(step, step_index=2, target_host="192.0.2.1")
    assert rec["workflow_phase"] == "web_assessment"
    assert rec["workflow_step_id"] == "PT-WEB-01"
    assert rec["parsed_summary"]["finding_count"] == 3
    validate_evidence_record(rec)
