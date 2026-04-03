from __future__ import annotations

import logging
import sys
from typing import Any

from pythonjsonlogger import jsonlogger


def setup_logging(config: dict[str, Any]) -> None:
    log_cfg = config.get("logging") or {}
    level_name = str(log_cfg.get("level", "INFO")).upper()
    level = getattr(logging, level_name, logging.INFO)
    use_json = bool(log_cfg.get("json_logs", True))

    root = logging.getLogger()
    root.setLevel(level)

    handler = logging.StreamHandler(sys.stderr)
    if use_json:
        fmt = "%(asctime)s %(name)s %(levelname)s %(message)s"
        handler.setFormatter(jsonlogger.JsonFormatter(fmt))
    else:
        handler.setFormatter(
            logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s")
        )

    root.handlers.clear()
    root.addHandler(handler)

    logging.getLogger("hexstrike_lab").debug("Structured logging initialized.")
