from __future__ import annotations

import re
from typing import Any


def _nmap_service_lines(stdout: str) -> list[str]:
    lines = []
    for line in stdout.splitlines():
        if re.match(r"^\d+/tcp\s+", line.strip()) or re.match(r"^\d+/udp\s+", line.strip()):
            lines.append(line.strip())
    return lines[:50]


def _nikto_hint(stdout: str) -> str:
    if not stdout.strip():
        return "No nikto stdout captured (dry-run or error)."
    return f"{len(stdout.splitlines())} lines; preview:\n\n```\n{stdout[:2500]}\n```"


def format_pipeline_markdown(doc: dict[str, Any]) -> str:
    """Generate summary markdown: executive summary, services, web, metadata."""
    target = doc.get("target") or {}
    host = target.get("host", "")
    orch = doc.get("orchestration") or {}
    profile = orch.get("profile", "")
    dry = orch.get("dry_run", True)
    started = orch.get("started_at", "")
    finished = orch.get("finished_at", "")
    lab = doc.get("lab") or {}

    nmap_lines: list[str] = []
    nikto_block = ""

    for step in orch.get("steps", []):
        ad = step.get("adapter", "")
        if ad == "nmap" and step.get("status") not in ("planned", "validation_error"):
            nmap_lines.extend(_nmap_service_lines(step.get("stdout", "")))
        if ad == "nikto" and step.get("status") not in ("planned", "validation_error"):
            nikto_block = _nikto_hint(step.get("stdout", ""))

    if not nmap_lines:
        for step in orch.get("steps", []):
            if step.get("adapter") == "nmap" and step.get("status") == "planned":
                nmap_lines = ["(Dry-run: no scan executed.)"]
                break

    exec_summary = (
        f"This report was generated for **authorized internal lab** use only. "
        f"Target **{host}** was assessed with profile **{profile}**. "
        f"Execution mode: **{'dry-run (planned commands only)' if dry else 'live tools'}**. "
        f"No exploitation logic is included in this pipeline."
    )

    services_section = (
        "### Discovered services (nmap)\n\n"
        + (
            "\n".join(f"- `{line}`" for line in nmap_lines)
            if nmap_lines
            else "- No parsed port lines (see raw output files under `output/raw/`)."
        )
    )

    web_section = "### Web findings overview (nikto)\n\n" + (
        nikto_block if nikto_block else "- Nikto not run, no output, or dry-run.\n"
    )

    meta = "\n".join(
        [
            "### Execution metadata",
            "",
            f"- **Lab**: {lab.get('name', '')}",
            f"- **Environment**: {lab.get('environment', '')}",
            f"- **Profile**: {profile}",
            f"- **Dry run**: {dry}",
            f"- **Started**: {started}",
            f"- **Finished**: {finished}",
            f"- **Schema version**: {doc.get('schema_version', '')}",
            "",
        ]
    )

    return "\n".join(
        [
            "## Executive summary",
            "",
            exec_summary,
            "",
            services_section,
            "",
            web_section,
            "",
            meta,
        ]
    )
