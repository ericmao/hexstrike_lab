# Lab 06 — MCP 與 hexstrike-ai 後端接通（Track B 起點）

**軸線：** Track B（外部 [hexstrike-ai](https://github.com/0x4m4/hexstrike-ai) MCP + 後端）。與 Track A（本 repo `hexstrike_lab`）並行，於 Lab11、Lab13 再次對照。

---

## 學習目標

- 啟動 **hexstrike-ai** 後端（`hexstrike_server.py`）並確認 **health**。
- 在 **Cursor／Claude Desktop** 等客戶端設定 **MCP**，使 `hexstrike_mcp.py` 能連到後端（參考上游 README 的 `args` 與埠號）。
- **必做（課程用 Kali）：** 安裝 **Ollama**，拉取並 smoke 測試 **`llama3`**，理解「LLM 決策」與「工具執行」分層。

## 授權與環境

- 僅在**隔離實驗室 VM**操作；本 Lab **不對外網任意目標**做掃描。
- **課程環境變體：** 若學校提供的是講師自訂「HexStrike CLI + `config.yaml`」而非上游 MCP，請以講師講義為準，並完成同等的「連通性驗收」。

## 操作步驟

1. 依上游文件 clone [hexstrike-ai](https://github.com/0x4m4/hexstrike-ai)、建立 venv、`pip install -r requirements.txt`。
2. 啟動：`python3 hexstrike_server.py`（埠號依課程約定，常見 `8888`）。
3. 驗證：`curl http://localhost:<port>/health`（或課程指定方式）。
4. 設定 MCP：將 `hexstrike_mcp.py` 與 `--server http://localhost:<port>` 寫入客戶端設定（見上游 README「Claude Desktop / Cursor」小節）。  
   - **Claude Code（Kali）JSON 範例與 NDR 拓樸（標的 192.168.1.203）：** [`labs/lab06/examples/`](examples/CLAUDE_CODE_MCP_JSON.md)（內含 [`claude_code_mcp_hexstrike.example.json`](examples/claude_code_mcp_hexstrike.example.json)）。
5. **Ollama + llama3（Kali 上）：**  
   `curl -fsSL https://ollama.com/install.sh | sh` → `ollama pull llama3` → `ollama run llama3 "Reply with exactly: OK"`。  
   確認服務監聽（常見 `11434`）；若 hexstrike-ai 需接 Ollama，依**上游 README**設定 base URL。  
6. 部署驗證（整機）：在 Kali 執行 repo 內 `bash scripts/verify_kali_lab_env.sh`（含 pytest、pipeline dry-run、ollama/llama3、可選 `8888/health`）。見 [docs/DEPLOY_KALI.md](../../docs/DEPLOY_KALI.md)。

## 觀察／除錯

- MCP 連線失敗：檢查後端是否 listening、防火牆、路徑是否為**絕對路徑**。
- 畫一張圖：**MCP Client → hexstrike_mcp → HTTP → hexstrike_server →（選）Ollama**。

## 驗收標準

- 提交：**連線示意圖** + **health 成功截圖或 log** + **`ollama list` 含 llama3** 與**一則** `ollama run llama3 …` 輸出節錄 + 一段話說明各元件責任。
- 口試：說明與本 repo `python -m hexstrike_lab` **無 MCP** 的差異。

## 講師提醒

- 勿在課堂預設開放學員自帶雲端 API Key；建議實驗室統一金鑰或僅 Ollama。
- 強調：本 Lab **只驗證環境**，下一個 Lab 才開始對**白名單標的**下任務。

## 與 hexstrike_lab 對照

| hexstrike_lab | hexstrike-ai（本 Lab） |
|---------------|-------------------------|
| CLI 直接呼叫適配器／編排 | LLM 經 MCP 驅動後端與多工具 |
| 無 HTTP 後端 | 通常有 HTTP server + MCP 橋接 |

## 建議 Cursor 提示詞（分段給）

**學員卡住時再给：**

1. 「請根據 hexstrike-ai 官方 README，列出我這台機器上 MCP 設定的檢查清單（路徑、Python、埠號、後端是否啟動）。」
2. 「解釋 FastMCP／stdio 與 `hexstrike_server` HTTP 之間的關係，用三句話。」

**勿**一次給完整設定檔；要求學員對照上游倉庫自行填路徑。
