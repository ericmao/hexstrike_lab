# hexstrike_lab

Authorized internal lab only. Includes **placeholder** scanners (`run`) and an optional **execution layer** (`assess`) that wraps `nmap` / `nikto` behind a unified adapter interface — see [docs/EXECUTION_LAYER.md](docs/EXECUTION_LAYER.md). Use `--dry-run` by default; pass `--execute` only on systems you are authorized to test.

## Clone (GitHub)

```bash
git clone https://github.com/ericmao/hexstrike_lab.git
cd hexstrike_lab
```

## Requirements

- Python 3.10+
- Kali Linux (or any Debian-based system)

## Setup (Kali)

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip make

cd hexstrike_lab
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

From the **project root** (directory that contains `configs/`):

```bash
python -m hexstrike_lab run --target 127.0.0.1 --pretty
```

### Tool orchestration (profiles)

Dry-run (planned commands only; **default**, safe):

```bash
python -m hexstrike_lab assess --target 192.0.2.1 --profile quick --pretty
```

Execute real tools (requires `nmap` / `nikto` on PATH):

```bash
python -m hexstrike_lab assess --target 192.0.2.1 --profile web --execute --pretty
```

Profiles are defined in `configs/profiles.yaml` (`quick`, `web`, `full`).

### End-to-end pipeline (raw + JSON + markdown + CTI stub)

```bash
chmod +x scripts/run_full_pipeline.sh
./scripts/run_full_pipeline.sh 192.0.2.1 quick
# Live: ./scripts/run_full_pipeline.sh 192.0.2.1 web --execute
```

Artifacts go under `output/raw/`, `output/json/`, `output/reports/`, `output/integration/`. See [docs/RUNBOOK_KALI.md](docs/RUNBOOK_KALI.md).

## Tests

```bash
make test
```

## License

Copyright © 2026 **ACTC** — *International Information Security Talent Cultivation and Promotion Association*（國際資訊安全人才培育與推廣協會）.  
This project is licensed under the [MIT License](LICENSE).

## Legal

Use only on systems you own or have explicit written permission to test.
