# Lab 07 — 範例繳交稿（授權標的 **192.168.1.203**）

> **性質：** 講師／助教參考範本；學員應自行執行並產出**自己的** log 與表格。  
> **環境：** 偵察自 **Kali `192.168.11.128`** 發起；與 [Lab06 NDR 拓樸](../../lab06/examples/TOPOLOGY_192.168.1.203_NDR.md) 可併陳於連線圖。  
> **原始工具輸出：** [nmap_192.168.1.203_top200.txt](nmap_192.168.1.203_top200.txt)、[nmap_192.168.1.203_common.txt](nmap_192.168.1.203_common.txt)、[phase2_http_192.168.1.203.txt](phase2_http_192.168.1.203.txt)

---

## 1. RTF 式提示詞（範例；若用 MCP 可貼入對話）

**角色：** 資深紅隊偵察員。  
**任務：** 在**僅限授權主機 `192.168.1.203`** 上完成 TCP 埠掃描；**禁止**掃描任何其他 IP 或網段。  
**輸出格式：** 表格列出 **IP、埠、狀態、服務推斷／指紋（若有）**；並列出建議在終端執行的 **nmap argv（單一主機）**。

**人工鎖定（務必保留）：** 若模型建議 `-A` 全網段或額外 IP，應拒絕並改寫為「`-Pn` + 明確埠範圍 + 單一 target」。

---

## 2. 掃描摘要表（由實際 nmap 整理）

| IP | 埠 | 狀態 | 服務（nmap 欄位） | 備註 |
|----|-----|------|------------------|------|
| 192.168.1.203 | 22/tcp | filtered | ssh | `no-response` |
| 192.168.1.203 | 80/tcp | filtered | http | `no-response` |
| 192.168.1.203 | 135/tcp | filtered | msrpc | `no-response` |
| 192.168.1.203 | 139/tcp | filtered | netbios-ssn | `no-response` |
| 192.168.1.203 | 443/tcp | filtered | https | `no-response` |
| 192.168.1.203 | 445/tcp | filtered | microsoft-ds | `no-response` |
| 192.168.1.203 | 3389/tcp | filtered | ms-wbt-server | `no-response` |
| 192.168.1.203 | 8080/tcp | filtered | http-proxy | `no-response` |
| 192.168.1.203 | 8443/tcp | filtered | https-alt | `no-response` |

**廣度掃描（top 200）：** 主機 **up**；200 個常見埠均為 **filtered**（無回應）。見 [nmap_192.168.1.203_top200.txt](nmap_192.168.1.203_top200.txt)。

**服務指紋／版本線索（Track C 選填）：** 本次 **無 open port**，nmap **未**取得版本字串；資料來源為 **2026-04-05** 之 `nmap -sV` 輸出（見 common 檔）。

---

## 3. 指令溯源附錄（完整 argv）

以下為**實際在 Kali 終端執行**之命令（非模型口述）：

```bash
nmap -Pn -sV -T4 --top-ports 200 192.168.1.203
```

```bash
nmap -Pn -p22,80,443,445,3389,8080,8443,135,139 -sV --reason 192.168.1.203
```

（若經 hexstrike-ai MCP 觸發，須另從 **server log** 複製**實際** argv；本範例為純本機終端對照。）

---

## 4. 第二階段 — 單一 IP 之 **80/tcp**（目錄／HTTP）

**範圍：** 僅 `http://192.168.1.203/`（不對其他主機、不做隱藏網段）。  
**結果：** TCP 連線失敗，與 nmap `80/tcp filtered` 一致。見 [phase2_http_192.168.1.203.txt](phase2_http_192.168.1.203.txt)。

---

## 5. Track C（P1）— 策略草擬 vs 人工刪減（範例）

| 步驟 | 內容 |
|------|------|
| **AI 草擬（示意）** | 「先對 `192.168.1.0/24` 做 ping sweep，再對 open host 全埠 `-p-`…」 |
| **人工刪減** | 刪除整段 `/24` 與全埠；改為**單一 IP** `192.168.1.203` + **有限埠集合**或 **top-ports**，符合 RoE。 |

---

## 6. 簡答 — `run_when`（規則式 profile）vs LLM 選工具

**問：** LLM 在何種情境下仍可能選錯工具或參數？  

**答（要點）：** YAML `run_when` 只在**已定義的欄位與條件**上分支，行為可預期、易做單元測試；LLM 會受提示詞歧義、訓練先驗、或「補完」未授權步驟影響，可能建議過寬的網段、`-O`、或與 log **不一致**的敘述。因此 Lab07 要求**指令溯源**與**白名單**，以稽核補足彈性帶來的不確定性。

---

## 7. 與 hexstrike_lab 對照（一句話）

`adaptive_web` 用 **schema 化條件**決定是否跑 nikto；本 Lab 用 **LLM + MCP** 決定 recon 深度——**可稽核性**靠 log／argv，**彈性**靠自然語言，兩者需在 RoE 下平衡。
