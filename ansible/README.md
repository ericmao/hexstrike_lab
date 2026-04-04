# Ansible — deploy hexstrike_lab to Kali

Prerequisites on your **control node**: Ansible 2.14+ (`ansible-playbook`).

```bash
cp inventory.example.ini inventory.ini
# edit ansible_host / ansible_user
ansible-playbook -i inventory.ini playbook.yml --ask-pass
# Lab VM 常用帳密為 kali/kali；建議之後 ssh-copy-id 改為金鑰登入並拿掉 --ask-pass。
```

**Full stack + Ollama (large download):**

```bash
ansible-playbook -i inventory.ini playbook_kali_full.yml --ask-pass --ask-become-pass -e install_ollama=true
```

Default Kali VM often uses the **same password for SSH and sudo** (`kali`/`kali`). Non-interactive example (lab only):

```bash
ansible-playbook -i inventory.ini playbook_kali_full.yml \
  -e ansible_ssh_pass=kali -e ansible_become_password=kali \
  -e install_ollama=true -e hexstrike_lab_git_force=true
```

Use `hexstrike_lab_git_force=true` if the tree was previously synced with **rsync** and `git` reports local modifications.

If **`ollama pull`** fails (DNS to `registry.ollama.ai`), fix lab resolver or proxy, then on Kali run `ollama pull llama3` manually; the playbook still exits **0** and prints a **WARN**.

- `playbook.yml` — **git clone** `hexstrike_lab` + venv only.
- `playbook_kali_full.yml` — imports `playbook.yml`, then optionally installs Ollama and runs `ollama pull llama3` as the SSH user.
- For rsync from your laptop, see [docs/DEPLOY_KALI.md](../docs/DEPLOY_KALI.md). On Kali run `bash scripts/verify_kali_lab_env.sh` to verify pytest, pipeline, Ollama, optional `/health`.
- **hexstrike-ai** is not installed by these playbooks; clone `~/hexstrike-ai` per upstream docs.
