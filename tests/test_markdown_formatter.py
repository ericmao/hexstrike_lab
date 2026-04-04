from hexstrike_lab.reports.markdown_formatter import format_pipeline_markdown


def test_format_pipeline_markdown_sections():
    doc = {
        "schema_version": "1.0.0",
        "target": {"host": "192.0.2.1"},
        "generated_at": "2026-01-01T00:00:00+00:00",
        "lab": {"name": "hexstrike_lab", "environment": "development"},
        "orchestration": {
            "profile": "quick",
            "dry_run": True,
            "started_at": "2026-01-01T00:00:00+00:00",
            "finished_at": "2026-01-01T00:00:01+00:00",
            "steps": [
                {
                    "adapter": "nmap",
                    "status": "planned",
                    "command": ["nmap", "192.0.2.1"],
                }
            ],
        },
        "findings": [],
    }
    md = format_pipeline_markdown(doc)
    assert "## Executive summary" in md
    assert "### Workflow steps" in md
    assert "### Findings summary" in md
    assert "Discovered services" in md
    assert "Web findings" in md
    assert "Execution metadata" in md
