import json
import subprocess
import sys
from pathlib import Path

import pytest

from hexstrike_lab.reports.markdown_formatter import generate_markdown_report


@pytest.fixture
def minimal_scan_doc() -> dict:
    return {
        "schema_version": "1.0.0",
        "target": {"host": "192.0.2.1"},
        "generated_at": "2026-01-01T00:00:00+00:00",
        "lab": {"name": "lab", "environment": "test"},
        "findings": [
            {
                "id": "f1",
                "scanner": "tool:nmap",
                "severity": "info",
                "title": "Tool run nmap",
                "evidence": {},
            }
        ],
        "orchestration": {
            "profile": "quick",
            "dry_run": False,
            "started_at": "2026-01-01T00:00:00+00:00",
            "finished_at": "2026-01-01T00:00:01+00:00",
            "steps": [
                {
                    "adapter": "nmap",
                    "status": "ok",
                    "duration_ms": 12.5,
                    "stdout": "",
                    "stderr": "",
                    "parsed": {
                        "data": {
                            "open_ports": [
                                {
                                    "port": 443,
                                    "protocol": "tcp",
                                    "service": "https",
                                    "detail": "test",
                                }
                            ]
                        }
                    },
                }
            ],
        },
    }


def test_generate_markdown_uses_parsed_ports_when_stdout_empty(minimal_scan_doc: dict):
    md = generate_markdown_report(minimal_scan_doc)
    assert "### Workflow steps" in md
    assert "### Findings summary" in md
    assert "443/tcp" in md
    assert "https" in md


def test_report_from_json_cli(tmp_path: Path, minimal_scan_doc: dict):
    jf = tmp_path / "report.json"
    jf.write_text(json.dumps(minimal_scan_doc), encoding="utf-8")
    out = tmp_path / "out.md"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "hexstrike_lab",
            "report",
            "from-json",
            "--input",
            str(jf),
            "--output",
            str(out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    assert out.is_file()
    assert "## Executive summary" in out.read_text(encoding="utf-8")
