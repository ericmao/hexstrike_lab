# Cursor Prompt Pack — hexstrike_lab

This document provides phase-based prompts for building an AI-assisted security testing framework in an **authorized internal lab** environment.

---

## Phase Overview

| Phase | Lab | Focus |
|------|-----|------|
| Phase 0 | Lab00 | Understand repo |
| Phase 1 | Lab01 | Adapter abstraction |
| Phase 2 | Lab02 | Orchestrator |
| Phase 3 | Lab03 | Pipeline |
| Phase 4 | Lab04 | RFP → scanning |
| Phase 5 | Lab05 | RFP → pentest |

### Track B — Lab06+ (hexstrike-ai MCP; external repo)

Uses **[hexstrike-ai](https://github.com/0x4m4/hexstrike-ai)** (MCP + `hexstrike_server.py`). **Not included in this repository.** Operate only in **authorized lab** environments. If your course uses a custom HexStrike CLI instead, see **課程環境變體** in each `labs/lab06+` file.

| Lab | Focus |
|-----|--------|
| Lab06 | MCP connectivity + server health + optional Ollama |
| Lab07 | Structured recon + **command traceability** |
| Lab08 | Scanner JSON analysis + **instructor-gated** verification |
| Lab09 | DVWA / authorized web testing + ethics |
| Lab10 | Python repair + JSON output + optional isolated shell demo |
| Lab11 | Capstone + Markdown report + compare `hexstrike_lab pipeline` |
| Lab12 | Rules of Engagement (RoE) |
| Lab13 | Map MCP/tool output to `evidence_record` |
| Lab14 | CI dry-run + `validate_scan_document` gate |
| Lab15 | Elective: cloud, bug-bounty rules, purple team, MCP–pipeline bridge |

Full steps and prompts: [`labs/README.md`](../labs/README.md) and `labs/labNN/cursor_prompts.md`.

---

## General Rules

- Use only authorized internal lab targets
- Avoid real production systems
- Focus on design, automation, and structured output
- Prefer modular, reusable architecture

---

## Phase 0 — Repo Understanding

### Prompt
Explain this repository as a modular security testing framework.

Focus on:
- folder structure
- execution flow
- role of profiles
- difference between run / assess / pipeline

---

## Phase 1 — Adapter

### Prompt
Create a ToolAdapter module.

Requirements:
- validate target input
- run tool via subprocess
- capture output
- return normalized JSON

---

## Phase 2 — Orchestrator

### Prompt
Design an Orchestrator.

Requirements:
- run discovery first
- decide next steps
- support profiles
- merge results

---

## Phase 3 — Pipeline

### Prompt
Create an end-to-end pipeline.

Steps:
- config
- orchestrator
- output collection
- JSON normalization
- markdown report

---

## Phase 4 — RFP Scanning

### Prompt
Translate vulnerability scanning requirements into a pipeline.

Include:
- discovery
- conditional web checks
- structured output

---

## Phase 5 — Pentest System

### Prompt
Design a multi-step testing workflow.

Requirements:
- decision-based flow
- structured evidence
- modular design

---

## Advanced — System Thinking

### Prompt
Refactor into a reusable execution framework.

Explain:
- architecture
- module responsibilities
- extension points

---

## Track B — Lab06+ (summary prompts for Cursor)

Use **after** Track A context is clear. Do not paste full lab sheets; open `labs/labNN/cursor_prompts.md` for 學習目標、授權、驗收.

### Lab06 — Environment
Help me verify hexstrike-ai MCP: checklist for Python path, server port, `hexstrike_mcp.py` args, and `GET /health`. Draw Client → MCP → HTTP → server.

### Lab07 — Recon
Given whitelist CIDR `<paste>`, draft an RTF-style prompt (role, task, table output). How do I trace actual argv from server logs?

### Lab08 — Reports
Summarize this Nuclei JSON severity distribution only (no live requests). What fields belong in an `evidence_record`-style row?

### Lab09 — DVWA
Explain filter behavior at Medium without running attacks. When are sqlmap tamper scripts justified under RoE?

### Lab10 — Code
List Python 2→3 breaking lines in this snippet before rewriting. Require JSON output schema `status`, `detail`, `timestamp`.

### Lab11 — Capstone
Outline a pentest report: required sections and evidence per section. Compare to `hexstrike_lab` `pipeline` JSON deliverables.

### Lab12 — RoE
Review this RoE draft for missing abort criteria and scope ambiguity (no offensive steps).

### Lab13 — Evidence
Map this log line to `hexstrike.pentest_evidence.v1` fields; list missing required fields.

### Lab14 — CI
Write a GitHub Actions step: run `pipeline` dry-run and validate latest `report.json` with `validate_scan_document`.

### Lab15 — Elective
(Choose sub-track) Design only: MCP invoking `python -m hexstrike_lab pipeline` with profile allowlist and no `shell=True`.
