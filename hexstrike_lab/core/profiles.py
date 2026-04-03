from __future__ import annotations

from pathlib import Path
from typing import Any

from hexstrike_lab.core.config import load_config


def load_profile_bundle(path: Path) -> dict[str, Any]:
    """Load configs/profiles.yaml: returns mapping profile_name -> profile dict."""
    data = load_config(path)
    profs = data.get("profiles")
    if not isinstance(profs, dict):
        raise ValueError("profiles file must contain top-level 'profiles' mapping")
    return profs


def get_profile(bundle: dict[str, Any], name: str) -> dict[str, Any]:
    if name not in bundle:
        raise KeyError(f"Unknown profile: {name!r}. Available: {sorted(bundle.keys())}")
    p = bundle[name]
    if not isinstance(p, dict):
        raise ValueError(f"Profile {name!r} must be a mapping")
    return p
