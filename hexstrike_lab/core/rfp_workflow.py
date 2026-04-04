from __future__ import annotations

from pathlib import Path
from typing import Any

from hexstrike_lab.core.config import load_config


def load_rfp_workflow(path: Path) -> dict[str, Any]:
    """Load configs/rfp_scan_requirements.yaml (or equivalent) for RFP traceability."""
    data = load_config(path)
    wf = data.get("workflow")
    if not isinstance(wf, dict):
        raise ValueError("RFP file must contain top-level 'workflow' mapping")
    return data


def workflow_profile_name(data: dict[str, Any]) -> str:
    """Return the profiles.yaml profile key referenced by the RFP workflow block."""
    wf = data.get("workflow")
    if not isinstance(wf, dict):
        raise ValueError("missing workflow")
    name = wf.get("profile")
    if not name or not isinstance(name, str):
        raise ValueError("workflow.profile must be a non-empty string")
    return name
