from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from hexstrike_lab.scanners.base import Scanner

logger = logging.getLogger(__name__)


class NetworkDiscoveryScanner(Scanner):
    """Placeholder: would run authorized discovery (e.g. ping sweep) in lab."""

    def run(self, target_host: str) -> dict[str, Any]:
        logger.info("network_discovery placeholder", extra={"target": target_host})
        return {
            "id": f"nd-{uuid.uuid4()}",
            "scanner": "network_discovery",
            "severity": "info",
            "title": "Placeholder network discovery",
            "description": "No live probes; authorized lab skeleton only.",
            "evidence": {
                "target": target_host,
                "not_executed": True,
                "would_run": ["placeholder_ping", "placeholder_port_list"],
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        }
