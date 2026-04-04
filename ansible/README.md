# Ansible — deploy hexstrike_lab to Kali

Prerequisites on your **control node**: Ansible 2.14+ (`ansible-playbook`).

```bash
cp inventory.example.ini inventory.ini
# edit ansible_host / ansible_user
ansible-playbook -i inventory.ini playbook.yml --ask-pass
# Lab VM 常用帳密為 kali/kali；建議之後 ssh-copy-id 改為金鑰登入並拿掉 --ask-pass。
```

- Uses **git clone**, not rsync. For rsync from your laptop, see [docs/DEPLOY_KALI.md](../docs/DEPLOY_KALI.md).
- **hexstrike-ai** is not installed by this playbook; install it separately in `~/hexstrike-ai` per upstream docs. Both can run on the same Kali.
