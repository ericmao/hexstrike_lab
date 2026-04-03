from hexstrike_lab.core.schema import SCAN_DOCUMENT_SCHEMA, validate_scan_document


def test_schema_has_title():
    assert SCAN_DOCUMENT_SCHEMA["title"] == "HexStrikeLabScanDocument"


def test_validate_minimal_document():
    doc = {
        "schema_version": "1.0.0",
        "target": {"host": "127.0.0.1"},
        "generated_at": "2026-04-03T00:00:00+00:00",
        "findings": [
            {
                "id": "x",
                "scanner": "network_discovery",
                "severity": "info",
                "title": "t",
                "evidence": {},
            }
        ],
    }
    validate_scan_document(doc)


def test_validate_with_orchestration():
    doc = {
        "schema_version": "1.0.0",
        "target": {"host": "192.0.2.1"},
        "generated_at": "2026-04-03T00:00:00+00:00",
        "orchestration": {"profile": "quick", "steps": []},
        "findings": [
            {
                "id": "exec-0-nmap",
                "scanner": "tool:nmap",
                "severity": "info",
                "title": "Tool run nmap",
                "description": "planned",
                "evidence": {"status": "planned"},
            }
        ],
    }
    validate_scan_document(doc)
