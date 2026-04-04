from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from hexstrike_lab import __version__
from hexstrike_lab.core.config import load_config
from hexstrike_lab.core.logging_setup import setup_logging
from hexstrike_lab.core.profiles import get_profile, load_profile_bundle
from hexstrike_lab.core.schema import validate_scan_document
from hexstrike_lab.execution.orchestrator import ExecutionOrchestrator
from hexstrike_lab.reports.markdown_formatter import generate_markdown_report
from hexstrike_lab.reports.normalizer import ReportNormalizer
from hexstrike_lab.scanners.network_discovery import NetworkDiscoveryScanner
from hexstrike_lab.scanners.web_metadata import WebMetadataScanner

_PROFILE_CHOICES = (
    "quick",
    "web",
    "full",
    "adaptive_web",
    "rfp_automated_scan",
    "pentest_lab",
)


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="hexstrike_lab",
        description="Authorized lab security testing framework (placeholders).",
    )
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    sub = p.add_subparsers(dest="command", required=True)

    run = sub.add_parser("run", help="Run placeholder scanners against a target host.")
    run.add_argument(
        "--target",
        required=True,
        help="Target host (hostname or IP) — lab placeholder only.",
    )
    run.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Path to YAML config (defaults to configs/default.yaml under CWD).",
    )
    run.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON to stdout.",
    )

    assess = sub.add_parser(
        "assess",
        help="Run profile-based tool execution (nmap/nikto); default is dry-run.",
    )
    assess.add_argument("--target", required=True, help="Lab target host or IP.")
    assess.add_argument(
        "--profile",
        required=True,
        choices=list(_PROFILE_CHOICES),
        help="Execution profile from configs/profiles.yaml.",
    )
    assess.add_argument(
        "--config",
        type=Path,
        default=None,
        help="Base YAML config (defaults to configs/default.yaml).",
    )
    assess.add_argument(
        "--profiles",
        type=Path,
        default=None,
        help="Profiles YAML (defaults to configs/profiles.yaml).",
    )
    assess.add_argument(
        "--execute",
        action="store_true",
        help="Actually run tools (otherwise dry-run: planned commands only).",
    )
    assess.add_argument(
        "--pretty",
        action="store_true",
        help="Pretty-print JSON to stdout.",
    )

    pipe = sub.add_parser(
        "pipeline",
        help="End-to-end: pre-check, assess, save raw/json, markdown, CTI stub.",
    )
    pipe.add_argument("--target", required=True, help="Lab target host or IP.")
    pipe.add_argument(
        "--profile",
        required=True,
        choices=list(_PROFILE_CHOICES),
        help="Profile from configs/profiles.yaml.",
    )
    pipe.add_argument("--config", type=Path, default=None)
    pipe.add_argument("--profiles", type=Path, default=None)
    pipe.add_argument(
        "--output-base",
        type=Path,
        default=Path("output"),
        help="Base dir for raw/, json/, reports/, integration/.",
    )
    pipe.add_argument(
        "--execute",
        action="store_true",
        help="Run real tools (otherwise dry-run; artifacts still written).",
    )

    rep = sub.add_parser(
        "report",
        help="Generate markdown from a saved scan document (e.g. pipeline report.json).",
    )
    rep_sub = rep.add_subparsers(dest="report_cmd", required=True)
    r_from = rep_sub.add_parser(
        "from-json",
        help="Validate JSON against the scan schema and write summary.md-style markdown.",
    )
    r_from.add_argument(
        "--input",
        type=Path,
        required=True,
        help="Path to report.json produced by the pipeline.",
    )
    r_from.add_argument(
        "--output",
        type=Path,
        default=None,
        help="Markdown output path (default: print to stdout).",
    )
    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)

    if args.command == "run":
        cfg_path = args.config
        if cfg_path is None:
            cfg_path = Path("configs/default.yaml")

        config: dict[str, Any] = load_config(cfg_path)
        setup_logging(config)

        target = args.target.strip()
        nd = NetworkDiscoveryScanner(config)
        wm = WebMetadataScanner(config)
        findings = [
            nd.run(target),
            wm.run(target),
        ]

        doc = ReportNormalizer(config).normalize(
            target_host=target,
            findings=findings,
        )
        validate_scan_document(doc)

        indent = 2 if args.pretty else None
        print(json.dumps(doc, indent=indent, ensure_ascii=False))
        return 0

    if args.command == "assess":
        cfg_path = args.config or Path("configs/default.yaml")
        prof_path = args.profiles or Path("configs/profiles.yaml")

        config: dict[str, Any] = load_config(cfg_path)
        setup_logging(config)

        bundle = load_profile_bundle(prof_path)
        profile = get_profile(bundle, args.profile)
        dry_run = not args.execute

        orch = ExecutionOrchestrator()
        orchestration = orch.run_profile(
            target=args.target.strip(),
            profile=profile,
            dry_run=dry_run,
        )
        doc = orch.merge_into_report(config, orchestration, args.target.strip())
        validate_scan_document(doc)

        indent = 2 if args.pretty else None
        print(json.dumps(doc, indent=indent, ensure_ascii=False))
        return 0

    if args.command == "pipeline":
        from hexstrike_lab.pipeline.runner import run_pipeline

        return run_pipeline(args)

    if args.command == "report":
        if args.report_cmd != "from-json":
            return 1
        doc = json.loads(args.input.read_text(encoding="utf-8"))
        validate_scan_document(doc)
        md = generate_markdown_report(doc)
        if args.output is not None:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(md, encoding="utf-8")
        else:
            sys.stdout.write(md)
        return 0

    return 1


if __name__ == "__main__":
    sys.exit(main())
