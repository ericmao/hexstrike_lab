from __future__ import annotations

from typing import Any

from hexstrike_lab.adapters.text_parsers import parse_nmap_stdout
from hexstrike_lab.execution.base import ToolAdapter, ToolResult
from hexstrike_lab.execution.targets import validate_lab_target


class NmapAdapter(ToolAdapter):
    """Service discovery via nmap (-sV); no exploit scripts."""

    name = "nmap"

    def validate_target(self, target: str) -> str:
        return validate_lab_target(target)

    def build_command(self, target: str, options: dict[str, Any]) -> list[str]:
        ports = str(options.get("ports", "22,80,443"))
        t = str(options.get("timing", "3")).lstrip("T")
        vint = int(options.get("version_intensity", 5))
        cmd = [
            "nmap",
            "-Pn",
            "-sV",
            "--version-intensity",
            str(vint),
            "-p",
            ports,
            f"-T{t}",
            target,
        ]
        return cmd

    def normalize_result(self, raw: ToolResult) -> dict[str, Any]:
        tool = parse_nmap_stdout(raw.stdout)
        return {
            "schema": "hexstrike.adapter.v1",
            "adapter": self.name,
            "run": {
                "status": raw.status,
                "exit_code": raw.exit_code,
                "message": raw.message,
            },
            "summary": {
                "kind": "nmap_service_discovery",
                "stdout_lines": len(raw.stdout.splitlines()),
                "open_port_count": tool["open_count"],
            },
            "data": tool,
            "artifacts": {
                "stdout_preview": raw.stdout[:2000],
                "stderr_preview": (raw.stderr or "")[:1000],
            },
        }
