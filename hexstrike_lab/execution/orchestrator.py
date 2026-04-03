from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from hexstrike_lab.execution.base import AdapterRegistry, ToolResult, default_registry
from hexstrike_lab.execution.runner import run_adapter


class ExecutionOrchestrator:
    """Runs registered tool adapters in sequence; merges results into a report."""

    def __init__(self, registry: AdapterRegistry | None = None) -> None:
        self._registry = registry or default_registry()

    def run_profile(
        self,
        *,
        target: str,
        profile: dict[str, Any],
        dry_run: bool = False,
    ) -> dict[str, Any]:
        steps_cfg = profile.get("steps", [])
        if not isinstance(steps_cfg, list):
            raise ValueError("profile.steps must be a list")

        out: dict[str, Any] = {
            "profile": profile.get("name", "unknown"),
            "target": target,
            "dry_run": dry_run,
            "started_at": datetime.now(timezone.utc).isoformat(),
            "steps": [],
        }

        for step in steps_cfg:
            if not isinstance(step, dict):
                raise ValueError("each step must be a mapping")
            name = step["adapter"]
            adapter = self._registry.create(name)
            opts = step.get("options") or {}
            if not isinstance(opts, dict):
                raise ValueError(f"options for {name} must be a mapping")
            timeout = float(step.get("timeout_sec", 120))
            retries = int(step.get("retries", 0))

            if dry_run:
                try:
                    cmd = adapter.dry_run(target, opts)
                except ValueError as e:
                    out["steps"].append(
                        {
                            "adapter": name,
                            "status": "validation_error",
                            "message": str(e),
                            "command": [],
                        }
                    )
                    continue
                out["steps"].append({"adapter": name, "status": "planned", "command": cmd})
                continue

            result = run_adapter(
                adapter, target, options=opts, timeout_sec=timeout, retries=retries
            )
            out["steps"].append(result.to_dict())

        out["finished_at"] = datetime.now(timezone.utc).isoformat()
        return out

    @staticmethod
    def merge_into_report(
        lab_config: dict[str, Any],
        orchestration: dict[str, Any],
        target_host: str,
    ) -> dict[str, Any]:
        """Build a single merged document: schema fields + orchestration + findings."""
        findings: list[dict[str, Any]] = []
        for i, step in enumerate(orchestration.get("steps", [])):
            adapter = step.get("adapter", "unknown")
            status = step.get("status", "unknown")
            if status == "planned":
                severity = "info"
            elif status in ("ok",):
                severity = "info"
            elif status in ("timeout", "error"):
                severity = "medium"
            else:
                severity = "low"

            findings.append(
                {
                    "id": f"exec-{i}-{adapter}",
                    "scanner": f"tool:{adapter}",
                    "severity": severity,
                    "title": f"Tool run {adapter}",
                    "description": step.get("message") or status,
                    "evidence": step,
                }
            )

        return {
            "schema_version": (lab_config.get("output") or {}).get("schema_version", "1.0.0"),
            "target": {"host": target_host, "notes": "authorized lab execution report"},
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "lab": dict(lab_config.get("lab") or {}),
            "orchestration": orchestration,
            "findings": findings,
        }
