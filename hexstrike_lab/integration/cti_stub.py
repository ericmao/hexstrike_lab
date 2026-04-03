from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def export_cti_stub(
    *,
    run_id: str,
    doc: dict[str, Any],
    output_path: Path,
) -> None:
    """
    Write a single NDJSON line for future ingestion into analytics / CTI platforms.
    Lab placeholder only — extend with your SIEM schema.
    """
    output_path.parent.mkdir(parents=True, exist_ok=True)
    record = {
        "schema": "hexstrike_lab.cti_stub.v1",
        "run_id": run_id,
        "target_host": (doc.get("target") or {}).get("host"),
        "profile": (doc.get("orchestration") or {}).get("profile"),
        "dry_run": (doc.get("orchestration") or {}).get("dry_run"),
        "generated_at": doc.get("generated_at"),
        "finding_count": len(doc.get("findings") or []),
        "payload_ref": "see normalized JSON report in output/json/",
    }
    with output_path.open("w", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")
