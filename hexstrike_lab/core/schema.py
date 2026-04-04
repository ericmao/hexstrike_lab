from __future__ import annotations

from typing import Any

from jsonschema import Draft202012Validator

from hexstrike_lab.core.evidence_schema import PENTEST_EVIDENCE_JSON_SCHEMA

SCAN_DOCUMENT_SCHEMA: dict[str, Any] = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "HexStrikeLabScanDocument",
    "type": "object",
    "additionalProperties": False,
    "required": ["schema_version", "target", "generated_at", "findings"],
    "properties": {
        "schema_version": {"type": "string", "pattern": r"^\d+\.\d+\.\d+$"},
        "target": {
            "type": "object",
            "additionalProperties": False,
            "required": ["host"],
            "properties": {
                "host": {"type": "string", "minLength": 1},
                "notes": {"type": "string"},
            },
        },
        "generated_at": {"type": "string", "format": "date-time"},
        "lab": {
            "type": "object",
            "additionalProperties": True,
        },
        "findings": {
            "type": "array",
            "items": {"$ref": "#/$defs/finding"},
        },
        "orchestration": {
            "type": "object",
            "description": "Optional HexStrike-style execution trace (tool runs, dry-run plans).",
            "additionalProperties": True,
        },
    },
    "$defs": {
        "finding": {
            "type": "object",
            "additionalProperties": False,
            "required": ["id", "scanner", "severity", "title", "evidence"],
            "properties": {
                "id": {"type": "string", "minLength": 1},
                "scanner": {"type": "string", "minLength": 1},
                "severity": {
                    "type": "string",
                    "enum": ["info", "low", "medium", "high", "critical"],
                },
                "title": {"type": "string"},
                "description": {"type": "string"},
                "evidence": {"type": "object", "additionalProperties": True},
                "evidence_record": {"$ref": "#/$defs/pentest_evidence"},
            },
        },
        "pentest_evidence": PENTEST_EVIDENCE_JSON_SCHEMA,
    },
}


def validate_scan_document(doc: dict[str, Any]) -> None:
    Draft202012Validator(SCAN_DOCUMENT_SCHEMA).validate(doc)
