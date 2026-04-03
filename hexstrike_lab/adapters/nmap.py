from __future__ import annotations

from typing import Any

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
        return {
            "summary": "nmap service discovery (lab)",
            "lines": len(raw.stdout.splitlines()),
            "preview": raw.stdout[:2000],
        }
