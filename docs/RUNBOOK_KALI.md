# Kali Linux runbook — hexstrike_lab

**Authorized internal lab assessments only.** No exploitation logic; discovery and controlled testing with normalized reporting.

## APT dependencies

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip make nmap nikto
```

Optional: `git` for version control.

### GitHub CLI (`gh`) — optional

For `gh auth login` and `gh repo` commands:

```bash
sudo apt update && sudo apt install -y gh
```

If you installed `gh` manually to `~/.local/bin` (or a symlink from `/tmp`), ensure `~/.local/bin` is on `PATH`, then run:

```bash
gh auth login
```

**Note:** A symlink to `/tmp/.../gh` breaks after reboot; prefer `apt install gh` or copy the binary when disk space allows.

## Python virtual environment

```bash
cd /path/to/hexstrike_lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

On Kali, use `pip install` **inside the venv** (PEP 668 blocks system-wide `pip`).

## End-to-end pipeline (single command)

From the project root (directory containing `configs/` and `output/`):

```bash
chmod +x scripts/run_full_pipeline.sh
./scripts/run_full_pipeline.sh 192.0.2.1 quick
```

- Default: **dry-run** (planned commands; raw + JSON + markdown + CTI stub still written).
- Live tools:

```bash
./scripts/run_full_pipeline.sh 192.0.2.1 web --execute
```

Equivalent Python invocation:

```bash
.venv/bin/python -m hexstrike_lab pipeline --target 192.0.2.1 --profile web --output-base ./output --execute
```

## Output layout

| Path | Content |
|------|---------|
| `output/raw/<run_id>/` | Per-step stdout/stderr text files |
| `output/json/<run_id>/report.json` | Normalized merged JSON |
| `output/reports/<run_id>/summary.md` | Executive summary + sections |
| `output/integration/cti_export_<run_id>.ndjson` | Stub line for future analytics ingestion |

Use **RFC 5737** documentation IPs (e.g. `192.0.2.x`) in examples, not production addresses.

## Tests

```bash
make test
```

## Troubleshooting

- **`nmap` / `nikto` not found**: install via `apt` or use dry-run until tools are available.
- **Permission denied on `run_full_pipeline.sh`**: run `chmod +x scripts/run_full_pipeline.sh`.
