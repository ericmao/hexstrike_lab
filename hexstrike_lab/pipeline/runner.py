from __future__ import annotations

import json
import logging
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from hexstrike_lab.core.config import load_config
from hexstrike_lab.core.logging_setup import setup_logging
from hexstrike_lab.core.profiles import get_profile, load_profile_bundle
from hexstrike_lab.core.schema import validate_scan_document
from hexstrike_lab.execution.orchestrator import ExecutionOrchestrator
from hexstrike_lab.integration.cti_stub import export_cti_stub
from hexstrike_lab.reports.markdown_formatter import format_pipeline_markdown

logger = logging.getLogger(__name__)


def precheck_environment(*, execute: bool) -> list[str]:
    """Return list of warning strings (empty if OK)."""
    warnings: list[str] = []
    if sys.version_info < (3, 10):
        warnings.append("Python 3.10+ recommended.")
    if execute:
        if not shutil.which("nmap"):
            warnings.append("nmap not found on PATH (required for live nmap steps).")
        if not shutil.which("nikto"):
            warnings.append("nikto not found on PATH (required for live nikto steps).")
    return warnings


def run_pipeline(args: Any) -> int:
    """Full pipeline: config, orchestrator, raw artifacts, JSON, markdown, CTI stub."""
    cfg_path = args.config or Path("configs/default.yaml")
    prof_path = args.profiles or Path("configs/profiles.yaml")
    output_base: Path = args.output_base
    target = args.target.strip()
    execute = bool(args.execute)

    for w in precheck_environment(execute=execute):
        logger.warning(w)

    config: dict[str, Any] = load_config(cfg_path)
    setup_logging(config)

    bundle = load_profile_bundle(prof_path)
    profile = get_profile(bundle, args.profile)

    run_id = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    raw_dir = output_base / "raw" / run_id
    json_dir = output_base / "json" / run_id
    reports_dir = output_base / "reports" / run_id
    integration_dir = output_base / "integration"
    raw_dir.mkdir(parents=True, exist_ok=True)
    json_dir.mkdir(parents=True, exist_ok=True)
    reports_dir.mkdir(parents=True, exist_ok=True)
    integration_dir.mkdir(parents=True, exist_ok=True)

    orch = ExecutionOrchestrator()
    orchestration = orch.run_profile(
        target=target,
        profile=profile,
        dry_run=not execute,
    )
    doc = orch.merge_into_report(config, orchestration, target)
    validate_scan_document(doc)

    for i, step in enumerate(orchestration.get("steps", [])):
        adapter = step.get("adapter", "unknown")
        fname = raw_dir / f"step_{i:02d}_{adapter}.txt"
        lines = [
            f"adapter={adapter}",
            f"status={step.get('status')}",
            "",
            "=== stdout ===",
            step.get("stdout") or "",
            "",
            "=== stderr ===",
            step.get("stderr") or "",
            "",
            "=== command ===",
            " ".join(step.get("command") or []),
        ]
        fname.write_text("\n".join(lines), encoding="utf-8")

    json_path = json_dir / "report.json"
    json_path.write_text(
        json.dumps(doc, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    md_path = reports_dir / "summary.md"
    md_path.write_text(format_pipeline_markdown(doc), encoding="utf-8")

    cti_path = integration_dir / f"cti_export_{run_id}.ndjson"
    export_cti_stub(run_id=run_id, doc=doc, output_path=cti_path)

    print(json.dumps({"status": "ok", "run_id": run_id, "paths": {
        "raw": str(raw_dir),
        "json": str(json_path),
        "report": str(md_path),
        "cti_stub": str(cti_path),
    }}, indent=2))
    return 0
