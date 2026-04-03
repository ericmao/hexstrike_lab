from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Any

from hexstrike_lab.scanners.base import Scanner

logger = logging.getLogger(__name__)


class WebMetadataScanner(Scanner):
    """Placeholder: would fetch headers/HTML metadata on authorized targets."""

    def run(self, target_host: str) -> dict[str, Any]:
        logger.info("web_metadata placeholder", extra={"target": target_host})
        return {
            "id": f"wm-{uuid.uuid4()}",
            "scanner": "web_metadata",
            "severity": "info",
            "title": "Placeholder web metadata check",
            "description": "No HTTP requests; authorized lab skeleton only.",
            "evidence": {
                "target": target_host,
                "not_executed": True,
                "would_request": f"https://{target_host}/",
                "timestamp": datetime.now(timezone.utc).isoformat(),
            },
        }
