# Lab 07 — 範例產物（標的 **192.168.1.203**）

對齊 [`../cursor_prompts.md`](../cursor_prompts.md)：結構化偵察、**指令溯源**、單一 IP 第二階段（80/tcp）、驗收用 Markdown 範本。

| 檔案 | 說明 |
|------|------|
| [LAB07_SAMPLE_SUBMISSION_192.168.1.203.md](LAB07_SAMPLE_SUBMISSION_192.168.1.203.md) | 完整範例繳交稿（表、argv、簡答、Track C） |
| [nmap_192.168.1.203_top200.txt](nmap_192.168.1.203_top200.txt) | `nmap --top-ports 200` 原始輸出 |
| [nmap_192.168.1.203_common.txt](nmap_192.168.1.203_common.txt) | 常見埠 `-sV --reason` 原始輸出 |
| [phase2_http_192.168.1.203.txt](phase2_http_192.168.1.203.txt) | 第二階段 HTTP 連線嘗試紀錄 |

**取得方式：** 在**已授權**之 Kali（範例自 `192.168.11.128`）上對**白名單** `192.168.1.203` 執行相同參數可重現；若標的服務變更，表格與狀態會不同，屬正常。
