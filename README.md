# hexstrike_lab

**Languages:** [繁體中文 README](README.zh-TW.md)

**Authorized internal lab only.** A small, modular framework for **structured security testing automation**: placeholder scanners, profile-driven tool runs (`nmap` / `nikto`), optional **conditional steps**, normalized **JSON** reports, **Markdown** summaries, and **evidence records** for controlled workflows.

Use only on systems you own or have **explicit written permission** to test. This project does not ship exploit modules.

---

## Table of contents

- [What’s in the box](#whats-in-the-box)
- [Requirements](#requirements)
- [Setup](#setup)
- [Run from the project root](#run-from-the-project-root)
- [Commands](#commands)
  - [`run`](#run--placeholder-scanners)
  - [`assess`](#assess--profile-based-tools)
  - [`pipeline`](#pipeline--end-to-end-artifacts)
  - [`report`](#report--markdown-from-json)
- [Profiles](#profiles)
- [Configuration](#configuration)
- [Pipeline output layout](#pipeline-output-layout)
- [RFP and pentest workflow docs](#rfp-and-pentest-workflow-docs)
- [Lab learning materials](#lab-learning-materials)
- [Further documentation](#further-documentation)
- [Tests](#tests)
- [License & legal](#license--legal)

---

## What’s in the box

| Area | Role |
|------|------|
| `hexstrike_lab/cli/` | CLI: `run`, `assess`, `pipeline`, `report` |
| `hexstrike_lab/scanners/` | In-process **placeholder** scanners (used by `run`) |
| `hexstrike_lab/adapters/` + `execution/` | **ToolAdapter** pattern: `subprocess`, validation, normalized `parsed` JSON |
| `hexstrike_lab/pipeline/` | Full run: raw transcripts, `report.json`, `summary.md`, manifest, CTI stub |
| `hexstrike_lab/reports/` | JSON → Markdown (`generate_markdown_report`) |
| `configs/` | `default.yaml`, `profiles.yaml`, RFP / pentest workflow YAML |
| `labs/` | Per-lab Cursor prompt snippets |
| `docs/` | Runbook, execution layer, Cursor prompt pack, instructor guide |

Execution details: [docs/EXECUTION_LAYER.md](docs/EXECUTION_LAYER.md).

---

## Requirements

- **Python 3.10+** (3.10 recommended; CI may use newer)
- For **live** `assess` / `pipeline` with `--execute`: **`nmap`** and **`nikto`** on `PATH`
- **Kali** or another Debian-based distro is typical for tool availability

---

## Setup

### Clone

```bash
git clone https://github.com/ericmao/hexstrike_lab.git
cd hexstrike_lab
```

### Virtualenv (recommended)

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Optional: Kali packages

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip make
# For live scans:
sudo apt install -y nmap nikto
```

See [docs/RUNBOOK_KALI.md](docs/RUNBOOK_KALI.md) for a fuller Kali-oriented runbook.

---

## Run from the project root

Commands expect a **current working directory** that contains **`configs/`** (usually the repo root).

```bash
cd hexstrike_lab
python -m hexstrike_lab --help
python -m hexstrike_lab <command> --help
```

---

## Commands

### `run` — placeholder scanners

Runs built-in **non-tool** placeholder scanners and prints one **schema-valid** JSON document to stdout.

```bash
python -m hexstrike_lab run --target 127.0.0.1 --pretty
```

| Flag | Meaning |
|------|---------|
| `--target` | Hostname or IP (lab target) |
| `--config` | Path to YAML (default: `configs/default.yaml`) |
| `--pretty` | Indent JSON |

---

### `assess` — profile-based tools

Loads a **profile** from `configs/profiles.yaml` and runs **nmap** / **nikto** steps (or **dry-run** planned commands only).

**Default is dry-run** (no real subprocess tools unless you pass `--execute`).

```bash
# Safe: print planned argv only
python -m hexstrike_lab assess --target 192.0.2.1 --profile quick --pretty

# Live: requires nmap/nikto on PATH
python -m hexstrike_lab assess --target 192.0.2.1 --profile web --execute --pretty
```

| Flag | Meaning |
|------|---------|
| `--target` | Lab host or IP |
| `--profile` | One of the [profiles](#profiles) |
| `--config` | Base config YAML (default: `configs/default.yaml`) |
| `--profiles` | Profiles file (default: `configs/profiles.yaml`) |
| `--execute` | Run real tools (otherwise dry-run) |
| `--pretty` | Indent JSON |

Output is a single JSON document: `orchestration`, `findings`, optional **`evidence_record`** per tool finding, etc.

---

### `pipeline` — end-to-end artifacts

Same orchestration as `assess`, then writes **files** under `--output-base` (default `output/`).

```bash
python -m hexstrike_lab pipeline --target 192.0.2.1 --profile quick --output-base output
python -m hexstrike_lab pipeline --target 192.0.2.1 --profile web --output-base output --execute
```

| Flag | Meaning |
|------|---------|
| `--target` | Lab host or IP |
| `--profile` | Profile name |
| `--output-base` | Root for `raw/`, `json/`, `reports/`, `integration/` |
| `--config` / `--profiles` | Same as `assess` |
| `--execute` | Live tools; without it, dry-run but artifacts still written |

**Shell helper** (uses `.venv/bin/python` if present):

```bash
chmod +x scripts/run_full_pipeline.sh
./scripts/run_full_pipeline.sh 192.0.2.1 quick
./scripts/run_full_pipeline.sh 192.0.2.1 web --execute
```

---

### `report` — Markdown from JSON

Regenerate a **summary Markdown** file from an existing **`report.json`** (schema-validated).

```bash
python -m hexstrike_lab report from-json --input output/json/<run_id>/report.json --output recap.md
python -m hexstrike_lab report from-json --input output/json/<run_id>/report.json   # stdout
```

---

## Profiles

Defined in **`configs/profiles.yaml`**. All names below are valid for `--profile` on `assess` and `pipeline`.

| Profile | Purpose |
|---------|---------|
| `quick` | Short nmap sweep |
| `web` | nmap (web ports) + nikto |
| `full` | Broader nmap + nikto |
| `adaptive_web` | nmap then **nikto only if** common web ports are open (`run_when`) |
| `rfp_automated_scan` | RFP-style port set + conditional nikto; see `configs/rfp_scan_requirements.yaml` |
| `pentest_lab` | Multi-step recon → enumeration → conditional web; metadata for **`evidence_record`**; see `configs/pentest_workflow.yaml` |

Edit timeouts, retries, and `options` in YAML to match your lab.

---

## Configuration

| File | Purpose |
|------|---------|
| `configs/default.yaml` | Lab metadata, logging, output schema version |
| `configs/profiles.yaml` | Profile definitions (`steps`, `adapter`, `run_when`, `pentest_phase`, …) |
| `configs/rfp_scan_requirements.yaml` | RFP requirement → workflow traceability |
| `configs/pentest_workflow.yaml` | Pentest phase design + profile binding |

---

## Pipeline output layout

After `pipeline`, each run uses a timestamp **`run_id`** (UTC, e.g. `20260404_123456`).

```
output/
├── raw/<run_id>/           # step_00_nmap.txt, … (stdout/stderr/command)
├── json/<run_id>/
│   ├── report.json         # full scan document
│   └── manifest.json       # phases, counts, paths
├── reports/<run_id>/
│   └── summary.md          # human-readable summary
└── integration/
    └── cti_export_<run_id>.ndjson
```

Stdout prints a small JSON object with `status`, `run_id`, and `paths`.

---

## RFP and pentest workflow docs

- **RFP scanning**: `configs/rfp_scan_requirements.yaml` maps requirement IDs to tools and artifacts; profile `rfp_automated_scan`.
- **Pentest-style lab workflow**: `configs/pentest_workflow.yaml` describes phases and decision points; profile `pentest_lab`.
- Loaders (for tooling/tests): `hexstrike_lab.core.rfp_workflow`, `hexstrike_lab.core.pentest_workflow`.

---

## Lab learning materials

Two tracks plus optional **Track C** depth (see [`labs/README.md`](labs/README.md), [`docs/TRACK_C_PENTEST.md`](docs/TRACK_C_PENTEST.md)):

- **Track A — `lab00` … `lab05`:** build and use **this** repo (`hexstrike_lab` CLI, adapters, pipeline, RFP/pentest YAML, evidence).
- **Track B — `lab06` … `lab15`:** **[hexstrike-ai](https://github.com/0x4m4/hexstrike-ai)** MCP + authorized lab scenarios, governance (RoE), evidence mapping, CI gates, and electives. **Not vendored here**; follow each `labs/labNN/cursor_prompts.md` **課程環境變體** if your course uses a different HexStrike CLI.
- **Track C — optional:** AI-augmented **pentest** depth (P1–P5: recon, web/Burp, exploit narrative, attack chain, red-team automation framing) woven into Lab07–11; does **not** replace Track B naming.

Central files:

- **`docs/CURSOR_PROMPT_PACK.md`** — Track A phases + Track B table and short prompts.
- **`docs/INSTRUCTOR_PROMPT_GUIDE.md`** — when to give prompts; **Track B safety gates** for Lab08–11; **Track C** instructor notes.

---

## Further documentation

- [docs/RUNBOOK_KALI.md](docs/RUNBOOK_KALI.md) — Kali setup and examples
- [docs/DEPLOY_KALI.md](docs/DEPLOY_KALI.md) — rsync / Ansible deploy; Ollama+llama3; `scripts/verify_kali_lab_env.sh`; coexistence with hexstrike-ai MCP
- [docs/TRACK_C_PENTEST.md](docs/TRACK_C_PENTEST.md) — optional pentest depth module (P1–P5)
- [docs/EXECUTION_LAYER.md](docs/EXECUTION_LAYER.md) — adapters, safety defaults, extension points
- [SECURITY.md](SECURITY.md) — responsible use

---

## Tests

```bash
make test
# or
python -m pytest tests/ -v
```

Convenience targets:

```bash
make run          # placeholder run
make assess-dry   # dry assess quick profile
make pipeline-dry # pipeline dry-run into ./output
```

---

## License & legal

Copyright © 2026 **ACTC** — *International Information Security Talent Cultivation and Promotion Association*（國際資訊安全人才培育與推廣協會）.  
Licensed under the [MIT License](LICENSE).

**Legal:** Use only on systems you own or have explicit written permission to test. No warranty; you are responsible for compliance with applicable laws and policies.
