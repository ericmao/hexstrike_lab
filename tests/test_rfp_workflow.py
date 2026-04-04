from pathlib import Path

import pytest

from hexstrike_lab.core.profiles import get_profile, load_profile_bundle
from hexstrike_lab.core.rfp_workflow import load_rfp_workflow, workflow_profile_name


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parents[1]


def test_rfp_workflow_resolves_to_existing_profile(project_root: Path):
    rfp_path = project_root / "configs" / "rfp_scan_requirements.yaml"
    prof_path = project_root / "configs" / "profiles.yaml"
    data = load_rfp_workflow(rfp_path)
    pname = workflow_profile_name(data)
    assert pname == "rfp_automated_scan"
    bundle = load_profile_bundle(prof_path)
    profile = get_profile(bundle, pname)
    assert profile["name"] == "rfp_automated_scan"
    steps = profile.get("steps", [])
    assert len(steps) == 2
    assert steps[0]["adapter"] == "nmap"
    assert steps[1]["adapter"] == "nikto"
    assert "run_when" in steps[1]


def test_rfp_requirements_list_non_empty(project_root: Path):
    data = load_rfp_workflow(project_root / "configs" / "rfp_scan_requirements.yaml")
    reqs = data.get("requirements")
    assert isinstance(reqs, list) and len(reqs) >= 1
