from __future__ import annotations

from typing import Any

from hexstrike_lab.adapters.text_parsers import parse_nikto_stdout
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
        tool = parse_nikto_stdout(raw.stdout)
        return {
            "schema": "hexstrike.adapter.v1",
            "adapter": self.name,
            "run": {
                "status": raw.status,
                "exit_code": raw.exit_code,
                "message": raw.message,
            },
            "summary": {
                "kind": "nikto_web_check",
                "stdout_lines": len(raw.stdout.splitlines()),
                "finding_count": tool["finding_count"],
                "truncated": tool["truncated"],
            },
            "data": tool,
            "artifacts": {
                "stdout_preview": raw.stdout[:2000],
                "stderr_preview": (raw.stderr or "")[:1000],
            },
        }
