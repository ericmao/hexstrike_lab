from __future__ import annotations

from datetime import datetime, timezone
from typing import Any

from jsonschema import Draft202012Validator

PENTEST_EVIDENCE_JSON_SCHEMA: dict[str, Any] = {
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema",
        "step_index",
        "target_host",
        "adapter",
        "execution_status",
        "collected_at",
        "tool",
        "parsed_summary",
        "artifacts",
    ],
    "properties": {
        "schema": {"const": "hexstrike.pentest_evidence.v1"},
        "step_index": {"type": "integer", "minimum": 0},
        "workflow_phase": {"type": ["string", "null"]},
        "workflow_step_id": {"type": "string"},
        "objective": {"type": "string"},
        "target_host": {"type": "string", "minLength": 1},
        "adapter": {"type": "string", "minLength": 1},
        "execution_status": {"type": "string", "minLength": 1},
        "collected_at": {"type": "string", "format": "date-time"},
        "tool": {
            "type": "object",
            "additionalProperties": True,
            "required": ["command"],
            "properties": {
                "command": {"type": "array", "items": {"type": "string"}},
                "exit_code": {},
                "duration_ms": {},
            },
        },
        "parsed_summary": {"type": "object", "additionalProperties": True},
        "artifacts": {
            "type": "array",
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["kind", "description"],
                "properties": {
                    "kind": {
                        "type": "string",
                        "enum": [
                            "raw_transcript",
                            "screenshot",
                            "export",
                            "note",
                            "pipeline_output",
                        ],
                    },
                    "path": {"type": "string"},
                    "description": {"type": "string"},
                },
            },
        },
        "analyst_notes": {"type": ["string", "null"]},
    },
}


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


def validate_evidence_record(record: dict[str, Any]) -> None:
    Draft202012Validator(PENTEST_EVIDENCE_JSON_SCHEMA).validate(record)


def build_evidence_record(
    step: dict[str, Any],
    *,
    step_index: int,
    target_host: str,
) -> dict[str, Any]:
    """Build a versioned evidence object for a single orchestration step (lab / authorized use)."""
    status = str(step.get("status", "unknown"))
    parsed = step.get("parsed") if isinstance(step.get("parsed"), dict) else {}
    data = parsed.get("data") if isinstance(parsed.get("data"), dict) else {}
    parsed_summary: dict[str, Any] = {}
    if "open_count" in data:
        parsed_summary["open_count"] = data["open_count"]
    if "finding_count" in data:
        parsed_summary["finding_count"] = data["finding_count"]
    if "open_ports" in data and isinstance(data["open_ports"], list):
        parsed_summary["open_ports_sample"] = data["open_ports"][:20]

    wf_phase = step.get("pentest_phase")
    if wf_phase is not None and not isinstance(wf_phase, str):
        wf_phase = str(wf_phase)

    rec: dict[str, Any] = {
        "schema": "hexstrike.pentest_evidence.v1",
        "step_index": step_index,
        "workflow_phase": wf_phase,
        "target_host": target_host,
        "adapter": str(step.get("adapter", "unknown")),
        "execution_status": status,
        "collected_at": step.get("collected_at") or _now_iso(),
        "tool": {
            "command": list(step.get("command") or []),
            "exit_code": step.get("exit_code"),
            "duration_ms": step.get("duration_ms"),
        },
        "parsed_summary": parsed_summary,
        "artifacts": list(step.get("evidence_artifacts") or []),
        "analyst_notes": step.get("analyst_notes"),
    }
    wsid = step.get("workflow_step_id")
    if wsid is not None:
        rec["workflow_step_id"] = str(wsid)
    obj = step.get("objective")
    if obj is not None:
        rec["objective"] = str(obj)
    validate_evidence_record(rec)
    return rec
