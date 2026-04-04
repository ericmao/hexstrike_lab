# Deploy `hexstrike_lab` on Kali (SSH) — coexistence with hexstrike-ai

Use only on **lab hosts you own or are authorized to manage** (e.g. `192.168.11.128`).

## Can both run on the same Kali?

**Yes.** They are separate trees and processes:

| Component | Typical path | Listens on | Role |
|-----------|--------------|------------|------|
| **hexstrike_lab** | `~/hexstrike_lab` | *(none by default)* | CLI: `python -m hexstrike_lab …` |
| **hexstrike-ai** | `~/hexstrike-ai` (separate clone) | **HTTP** e.g. `8888` | `hexstrike_server.py`; MCP bridge uses stdio client → that URL |

- **No port conflict:** `hexstrike_lab` does not start a network server for normal `run` / `assess` / `pipeline`.
- **Separate venvs:** use `~/hexstrike_lab/.venv` and `~/hexstrike-ai/hexstrike-env` (or whatever the upstream README uses).
- **MCP client** (Cursor on your laptop) should point `--server` at `http://192.168.11.128:8888` **only if** the server binds `0.0.0.0` and your lab firewall allows it; otherwise run MCP client on the same machine as the server.

**Quick check on Kali after both are installed:**

```bash
# hexstrike_lab (from repo root, venv active)
cd ~/hexstrike_lab && . .venv/bin/activate && python -m hexstrike_lab run --target 127.0.0.1

# hexstrike-ai (separate terminal; follow upstream docs)
curl -s http://127.0.0.1:8888/health
```

---

## One-line `rsync` (from your laptop, repo root)

Run inside your **local** `hexstrike_lab` clone (directory that contains `configs/`).

**Without deleting extra files on the server** (safer):

```bash
rsync -avz -e ssh --progress --exclude '.git/' --exclude '.venv/' --exclude 'output/' --exclude '__pycache__/' --exclude '.pytest_cache/' ./ kali@192.168.11.128:~/hexstrike_lab/
```

Then on Kali:

```bash
ssh kali@192.168.11.128
cd ~/hexstrike_lab && python3 -m venv .venv && . .venv/bin/activate && pip install -r requirements.txt
python -m hexstrike_lab run --target 127.0.0.1 --pretty
```

**Mirror delete** (makes remote match local — can remove files you deleted locally):

```bash
rsync -avz -e ssh --delete --exclude '.git/' --exclude '.venv/' --exclude 'output/' ./ kali@192.168.11.128:~/hexstrike_lab/
```

---

## Ansible

From a machine with Ansible installed:

```bash
cd ansible
cp inventory.example.ini inventory.ini
# Edit inventory.ini: set ansible_host=192.168.11.128 ansible_user=kali
ansible-playbook -i inventory.ini playbook.yml
```

This **git-clones** (or updates) `hexstrike_lab` on the target and creates `.venv` + `pip install -r requirements.txt`. It does **not** install hexstrike-ai; clone that repo separately per [hexstrike-ai](https://github.com/0x4m4/hexstrike-ai).

---

## hexstrike-ai on the same host (manual, upstream)

```bash
cd ~
git clone https://github.com/0x4m4/hexstrike-ai.git
cd hexstrike-ai
python3 -m venv hexstrike-env && source hexstrike-env/bin/activate
pip install -r requirements.txt
python3 hexstrike_server.py --port 8888
```

Configure your MCP client `hexstrike_mcp.py` with `--server http://<kali-ip>:8888` as in upstream README.
