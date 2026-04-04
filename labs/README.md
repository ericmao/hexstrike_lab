# Labs index

Three layers (read **Track C** naming below):

| Track | Labs | Focus |
|-------|------|--------|
| **A** | [lab00](lab00) – [lab05](lab05) | Build and use **this repo** (`hexstrike_lab`): adapters, orchestrator, pipeline, RFP/pentest YAML, evidence schema. |
| **B** | [lab06](lab06) – [lab15](lab15) | **hexstrike-ai** MCP + authorized lab scenarios; governance and integration with Track A. |
| **C** | *(cross-cutting)* | **AI-Augmented Pentest** depth: exploit mindset, Burp/chain/flag-style objectives. Mapped in [docs/TRACK_C_PENTEST.md](../docs/TRACK_C_PENTEST.md) (P1–P5); reinforced inside Lab07–11. |

**External dependency (Track B):** [0x4m4/hexstrike-ai](https://github.com/0x4m4/hexstrike-ai) — not vendored here. Your course may use a different “HexStrike” CLI; see **課程環境變體** in each `lab06+` file.

| Lab | Topic |
|-----|--------|
| 06 | MCP + server + **Ollama / llama3** (see lab file) |
| 07 | Structured recon + command traceability + **Track C P1** |
| 08 | Nuclei (or similar) JSON + gated verification |
| 09 | DVWA / authorized web + **Burp / P2** |
| 10 | Python modernization + optional shell + **P3** |
| 11 | Capstone CTF-style + report vs `pipeline` + **P4 chain** |
| 12 | Rules of Engagement (RoE) |
| 13 | Evidence mapping to `evidence_record` |
| 14 | CI dry-run + schema gate |
| 15 | Elective: cloud, BBY rules, purple team, or MCP–pipeline bridge |

**Deploy + verify on Kali:** [docs/DEPLOY_KALI.md](../docs/DEPLOY_KALI.md) — includes `scripts/verify_kali_lab_env.sh` (pytest, pipeline, Ollama/llama3, optional `/health`).

Central prompts: [docs/CURSOR_PROMPT_PACK.md](../docs/CURSOR_PROMPT_PACK.md).  
Instructor timing: [docs/INSTRUCTOR_PROMPT_GUIDE.md](../docs/INSTRUCTOR_PROMPT_GUIDE.md).
