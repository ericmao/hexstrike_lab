# Execution layer (HexStrike-style)

This module is for **authorized internal lab assessments only**. It does not include exploit modules; it focuses on **discovery**, **controlled testing**, and **normalized reporting**.

## Why this layer matters (HexStrike-style value)

### Unified execution

External tools (`nmap`, `nikto`, ...) are wrapped behind a single `ToolAdapter` interface. Every tool is invoked with `subprocess` (no shell), the same timeout/retry policy, and the same `ToolResult` shape. Operators maintain one orchestration path instead of a pile of ad-hoc scripts.

### Repeatable workflow

**Profiles** (`quick`, `web`, `full`) encode which steps run, timeouts, and retries. Version-controlled YAML makes runs **reproducible** across lab sessions and teammates.

### Normalized outputs

Each adapter returns a **JSON-friendly** `ToolResult` dict (stdout/stderr, exit code, duration, parsed summary). The orchestrator merges steps into one report with **one schema**, suitable for dashboards, CI gates, or later HexStrike integration.

### Extensibility

New tools are registered in `AdapterRegistry` (`hexstrike_lab.execution.base.default_registry`). Add a class implementing `ToolAdapter`, register it, and reference it in `configs/profiles.yaml` — no change to the core orchestrator loop.

## Safety defaults

- `--dry-run` (default for `assess`): prints planned commands only; **no** subprocess.
- `--execute`: required to run real tools; use only on systems you own or are explicitly authorized to test.
- Targets are validated via `validate_lab_target()` (no shell metacharacters, no path-like strings).

## Requirements

- `nmap` and `nikto` on `PATH` when using `--execute`.
