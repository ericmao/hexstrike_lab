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


def _nmap_lines_from_parsed(step: dict[str, Any]) -> list[str]:
    parsed = step.get("parsed") if isinstance(step.get("parsed"), dict) else {}
    data = parsed.get("data") if isinstance(parsed.get("data"), dict) else {}
    ports = data.get("open_ports")
    if not isinstance(ports, list):
        return []
    lines: list[str] = []
    for entry in ports:
        if not isinstance(entry, dict) or "port" not in entry:
            continue
        proto = entry.get("protocol") or "tcp"
        svc = entry.get("service") or ""
        detail = (entry.get("detail") or "").strip()
        tail = f" {detail}" if detail else ""
        lines.append(f"{entry['port']}/{proto} open {svc}{tail}".strip())
    return lines[:50]


def _workflow_markdown(steps: list[dict[str, Any]]) -> str:
    if not steps:
        return "### Workflow steps\n\n- No orchestration steps.\n"
    header = "| Step | Adapter | Status | Duration (ms) | Note |\n| --- | --- | --- | --- | --- |"
    rows: list[str] = [header]
    for i, s in enumerate(steps):
        ad = s.get("adapter", "")
        st = s.get("status", "")
        dur = s.get("duration_ms")
        dur_s = "" if dur is None else str(dur)
        msg = (s.get("message") or "").replace("|", "\\|")
        if len(msg) > 120:
            msg = msg[:117] + "..."
        rows.append(f"| {i + 1} | {ad} | {st} | {dur_s} | {msg} |")
    return "### Workflow steps\n\n" + "\n".join(rows) + "\n"


def _findings_markdown(findings: list[dict[str, Any]], *, limit: int = 30) -> str:
    if not findings:
        return "### Findings summary\n\n- No findings recorded.\n"
    lines = ["### Findings summary\n"]
    for f in findings[:limit]:
        sev = f.get("severity", "")
        scanner = f.get("scanner", "")
        title = (f.get("title") or "").replace("|", "\\|")
        fid = f.get("id", "")
        desc = f.get("description")
        extra = f" — {desc}" if desc else ""
        lines.append(f"- **{sev}** `{fid}` [{scanner}] {title}{extra}")
    if len(findings) > limit:
        lines.append(f"\n*({len(findings) - limit} more omitted)*\n")
    else:
        lines.append("")
    return "\n".join(lines) + "\n"


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
    nikto_skipped_reason = ""

    for step in orch.get("steps", []):
        ad = step.get("adapter", "")
        if ad == "nmap" and step.get("status") not in ("planned", "validation_error"):
            nmap_lines.extend(_nmap_service_lines(step.get("stdout", "")))
            if not nmap_lines:
                nmap_lines.extend(_nmap_lines_from_parsed(step))
        if ad == "nikto" and step.get("status") == "skipped":
            nikto_skipped_reason = step.get("message") or "skipped by workflow condition"
        if ad == "nikto" and step.get("status") not in (
            "planned",
            "validation_error",
            "skipped",
        ):
            nikto_block = _nikto_hint(step.get("stdout", ""))

    if not nmap_lines:
        for step in orch.get("steps", []):
            if step.get("adapter") == "nmap" and step.get("status") == "planned":
                nmap_lines = ["(Dry-run: no scan executed.)"]
                break
            if step.get("adapter") == "nmap" and step.get("status") not in (
                "planned",
                "validation_error",
            ):
                parsed_lines = _nmap_lines_from_parsed(step)
                if parsed_lines:
                    nmap_lines = parsed_lines
                    break

    steps_list = orch.get("steps", [])
    workflow_section = _workflow_markdown(steps_list) if isinstance(steps_list, list) else ""
    findings_section = _findings_markdown(doc.get("findings") or [])

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

    if nikto_skipped_reason:
        web_body = f"- **Skipped** (conditional workflow): {nikto_skipped_reason}\n"
    elif nikto_block:
        web_body = nikto_block
    else:
        web_body = "- Nikto not run, no output, or dry-run.\n"

    web_section = "### Web findings overview (nikto)\n\n" + web_body

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
            workflow_section,
            findings_section,
            services_section,
            "",
            web_section,
            "",
            meta,
        ]
    )


def generate_markdown_report(doc: dict[str, Any]) -> str:
    """Build a markdown summary from a scan document dict (e.g. ``report.json``)."""
    return format_pipeline_markdown(doc)
