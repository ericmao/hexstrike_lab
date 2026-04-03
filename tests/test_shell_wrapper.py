import subprocess
from pathlib import Path

import pytest


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_run_full_pipeline_script_invokes_python(project_root: Path, tmp_path: Path):
    script = project_root / "scripts" / "run_full_pipeline.sh"
    proc = subprocess.run(
        [str(script), "192.0.2.1", "quick", "--output-base", str(tmp_path)],
        cwd=str(project_root),
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stderr + proc.stdout
    assert "run_id" in proc.stdout
