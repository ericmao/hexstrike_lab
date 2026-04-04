# Instructor Prompt Guide

**Answer outline & rubric (instructor-only):** [INSTRUCTOR_ANSWER_OUTLINE.md](INSTRUCTOR_ANSWER_OUTLINE.md)

## Teaching Strategy

Do **NOT** give prompts immediately.

Instead:

1. Let students attempt design
2. Introduce prompt when stuck
3. Compare results

---

## Prompt Timing

| Phase | When to give |
|------|-------------|
| Phase 1 | after first failed script |
| Phase 2 | when logic becomes messy |
| Phase 3 | when output is inconsistent |
| Phase 4 | when mapping RFP |
| Phase 5 | when attack flow unclear |

### Track B (Lab06+ — hexstrike-ai MCP)

| Situation | When to give prompts / handouts |
|-----------|----------------------------------|
| Lab06 | MCP or server will not connect — give **checklist** (paths, venv, port, firewall); not a full config dump |
| Lab07 | Student cannot find **real argv** in logs — give **where to look** in `hexstrike_server` / tool stdout, one hint at a time |
| Lab08 | Student wants to run AI-generated exploit code immediately — **withhold** prompt until **RoE / instructor approval** step is done |
| Lab09 | Payloads drift to **non-whitelist URLs** — give **scope lock** sentence for system prompt; stop lab if repeated |
| Lab10 | Reverse-shell attempts outside **isolated VLAN** — **stop exercise**; switch to JSON-only verification |
| Lab11 | Report is **hallucinated** (no matching logs) — give **evidence-per-section** template only |
| Lab12 | RoE is one paragraph — give **structured blank form**, not filled example |
| Lab13 | Table is empty — give **one sample row** mapped from a fake log line |
| Lab14 | CI fails on `run_id` path — give **find-latest-json** snippet, not entire workflow |
| Lab15 | Scope creep on cloud or BBY — **re-read RoE** handout before any Cursor prompt |

### Safety gates (Track B)

- **Lab08 verification script** and **Lab09 sqlmap**: require **explicit instructor approval** before execution.
- **Lab10** reverse shell: **optional**; default grade on code review + JSON output only.
- **Lab11** capstone: whitelist target IP issued by instructor only.

### Track C (Pentest depth — see [TRACK_C_PENTEST.md](TRACK_C_PENTEST.md))

- **P1 / Lab07**: AI-generated recon scripts must be **human-trimmed** before execution; re-check argv against RoE.
- **P2 / Lab09**: Burp/raw-request evidence is **manual proof**; do not accept generic AI prose without a saved request excerpt.
- **P3–P4 / Lab10–11**: Attack-chain table and optional flags require **mapped logs**; same hallucination rules as Lab11 Track B.

---

## Key Teaching Message

We are **not** using AI to hack.

We are using AI to build **systems** that perform **security testing** — with clear scope, reproducible workflows, and defensible evidence — in **authorized** environments only.
