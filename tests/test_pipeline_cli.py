import json
import subprocess
import sys
from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_pipeline_dry_run_writes_artifacts(project_root: Path, tmp_path: Path, monkeypatch):
    monkeypatch.chdir(project_root)
    out = tmp_path / "out"
    proc = subprocess.run(
        [
            sys.executable,
            "-m",
            "hexstrike_lab",
            "pipeline",
            "--target",
            "192.0.2.1",
            "--profile",
            "quick",
            "--output-base",
            str(out),
        ],
        capture_output=True,
        text=True,
        check=False,
    )
    assert proc.returncode == 0, proc.stderr
    summary = json.loads(proc.stdout)
    assert summary["status"] == "ok"
    run_id = summary["run_id"]
    assert (out / "json" / run_id / "report.json").is_file()
    assert (out / "reports" / run_id / "summary.md").is_file()
    assert (out / "integration" / f"cti_export_{run_id}.ndjson").is_file()
