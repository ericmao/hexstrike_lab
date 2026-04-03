from __future__ import annotations

from typing import Any

from hexstrike_lab.execution.base import ToolAdapter, ToolResult
from hexstrike_lab.execution.targets import validate_lab_target


class NiktoAdapter(ToolAdapter):
    """Web security checks via nikto against a controlled lab URL."""

    name = "nikto"

    def validate_target(self, target: str) -> str:
        return validate_lab_target(target)

    def build_command(self, target: str, options: dict[str, Any]) -> list[str]:
        ssl = bool(options.get("ssl", True))
        port = int(options.get("port", 443))
        scheme = "https" if ssl else "http"
        host = target
        if ":" in host and host.count(":") > 1:
            url = f"{scheme}://[{host}]:{port}/"
        else:
            url = f"{scheme}://{host}:{port}/"
        return [
            "nikto",
            "-h",
            url,
            "-maxtime",
            str(int(options.get("maxtime_sec", 300))),
        ]

    def normalize_result(self, raw: ToolResult) -> dict[str, Any]:
        return {
            "summary": "nikto web check (lab)",
            "lines": len(raw.stdout.splitlines()),
            "preview": raw.stdout[:2000],
        }
