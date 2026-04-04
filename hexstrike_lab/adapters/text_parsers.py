from __future__ import annotations

import re
from typing import Any

_NMAP_OPEN = re.compile(
    r"^(\d+)/(tcp|udp)\s+open\s+(\S+)\s*(.*)$",
    re.IGNORECASE,
)


def parse_nmap_stdout(stdout: str) -> dict[str, Any]:
    """Extract open ports/services from default nmap -sV style text output."""
    open_ports: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        line = line.rstrip()
        m = _NMAP_OPEN.match(line.strip())
        if not m:
            continue
        port, proto, service, detail = m.groups()
        open_ports.append(
            {
                "port": int(port),
                "protocol": proto.lower(),
                "service": service,
                "detail": detail.strip(),
            }
        )
    return {"open_ports": open_ports, "open_count": len(open_ports)}


def parse_nikto_stdout(stdout: str, *, max_findings: int = 200) -> dict[str, Any]:
    """Collect nikto '+ ' report lines as structured findings."""
    findings: list[str] = []
    for line in stdout.splitlines():
        s = line.strip()
        if s.startswith("+ "):
            findings.append(s[2:].strip())
    truncated = len(findings) > max_findings
    if truncated:
        findings = findings[:max_findings]
    return {
        "findings": findings,
        "finding_count": len(findings),
        "truncated": truncated,
    }
