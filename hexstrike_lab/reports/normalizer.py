from __future__ import annotations

from datetime import datetime, timezone
from typing import Any


class ReportNormalizer:
    """Merge scanner outputs into one normalized JSON document."""

    def __init__(self, config: dict[str, Any]) -> None:
        self._config = config

    def normalize(
        self,
        *,
        target_host: str,
        findings: list[dict[str, Any]],
    ) -> dict[str, Any]:
        out_cfg = self._config.get("output") or {}
        version = str(out_cfg.get("schema_version", "1.0.0"))
        lab = self._config.get("lab") or {}

        return {
            "schema_version": version,
            "target": {"host": target_host, "notes": "authorized lab placeholder"},
            "generated_at": datetime.now(timezone.utc).isoformat(),
            "lab": dict(lab),
            "findings": findings,
        }
