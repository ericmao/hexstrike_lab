from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


@dataclass
class ToolResult:
    """Normalized output for one tool invocation (authorized lab)."""

    adapter: str
    target: str
    status: str  # ok | error | timeout | validation_error | skipped
    exit_code: int | None
    duration_ms: float
    stdout: str
    stderr: str
    message: str | None = None
    command: list[str] = field(default_factory=list)
    parsed: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "adapter": self.adapter,
            "target": self.target,
            "status": self.status,
            "exit_code": self.exit_code,
            "duration_ms": round(self.duration_ms, 3),
            "stdout": self.stdout,
            "stderr": self.stderr,
            "message": self.message,
            "command": self.command,
            "parsed": self.parsed,
            "collected_at": datetime.now(timezone.utc).isoformat(),
        }


class ToolAdapter(ABC):
    """Plugin interface: one external security tool."""

    name: str

    @abstractmethod
    def validate_target(self, target: str) -> str:
        """Return normalized target or raise ValueError."""

    @abstractmethod
    def build_command(self, target: str, options: dict[str, Any]) -> list[str]:
        """Argv list; never use shell=True."""

    @abstractmethod
    def normalize_result(self, raw: ToolResult) -> dict[str, Any]:
        """Return tool-specific JSON-friendly summary inside parsed."""

    def dry_run(self, target: str, options: dict[str, Any]) -> list[str]:
        return self.build_command(self.validate_target(target), options)


class AdapterRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, type[ToolAdapter]] = {}

    def register(self, name: str, cls: type[ToolAdapter]) -> None:
        self._adapters[name] = cls

    def create(self, name: str) -> ToolAdapter:
        if name not in self._adapters:
            raise KeyError(f"Unknown adapter: {name}")
        return self._adapters[name]()


def default_registry() -> AdapterRegistry:
    from hexstrike_lab.adapters.nmap import NmapAdapter
    from hexstrike_lab.adapters.nikto import NiktoAdapter

    r = AdapterRegistry()
    r.register("nmap", NmapAdapter)
    r.register("nikto", NiktoAdapter)
    return r
