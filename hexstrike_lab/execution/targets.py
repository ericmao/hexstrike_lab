from __future__ import annotations

import ipaddress
import re

_HOST_RE = re.compile(r"^[a-zA-Z0-9]([a-zA-Z0-9.-]{0,253}[a-zA-Z0-9])?$")


def validate_lab_target(raw: str) -> str:
    """Validate hostname or IP for lab targets; reject shell metacharacters and paths."""
    s = raw.strip()
    if not s or len(s) > 253:
        raise ValueError("Invalid target: empty or too long")
    for bad in ";|&$`<>(){}[]*?\\'\"":
        if bad in s:
            raise ValueError(f"Invalid target: forbidden character {bad!r}")
    if "/" in s or ".." in s:
        raise ValueError("Invalid target: path-like strings not allowed")
    try:
        ipaddress.ip_address(s)
        return s
    except ValueError:
        pass
    if _HOST_RE.match(s):
        return s
    raise ValueError("Invalid target: not a valid hostname or IP")
