# Lab 13 — 證據鏈與合規對照（對齊 `evidence_record`）

**定位：** 銜接 Track A **Lab05** 與 Track B MCP 輸出。

---

## 學習目標

- 選擇 **同一授權事件**（例如 Lab08 的 Nuclei 驗證或 Lab11 的某一發現），產出兩種表述：
  1. **MCP／工具原始脈絡**（log、截圖、對話節錄）；
  2. 對齊本 repo **`hexstrike.pentest_evidence.v1`** 的結構化欄位（可手填表格或 JSON 草稿）。
- 說明哪些欄位在 MCP 流程中**容易缺漏**（例如 `collected_at`、`workflow_step_id`）。

## 授權與環境

- 僅使用本課程已授權之 log 與截圖；**禁止**含真實客戶 PII。
- 可閱讀原始碼：[`hexstrike_lab/core/evidence_schema.py`](../../hexstrike_lab/core/evidence_schema.py)。

## 操作步驟

1. 列出該事件的 **時間線**（T0 指令、T1 輸出、T2 人工判讀）。
2. 填寫對照表：`schema`、`adapter` 或等效工具名、`execution_status`、`tool.command`、`parsed_summary`、`artifacts`（若無檔案則註明「僅記憶體輸出」）。
3. （選）用 `python -m hexstrike_lab report from-json` 將**手寫**之最小 `report.json`（僅含 findings + evidence_record）轉成 Markdown，檢視可讀性。

## 觀察／除錯

- 若 `command` 陣列無法還原：討論 **MCP 工具封裝**應如何強制記錄 argv。
- 比對：`merge_into_report` 自動產生的 `evidence_record` 與你手填的差異。

## 驗收標準

- 提交：**對照表** + **200 字**：若要送稽核，你會補哪三個欄位？

## 講師提醒

- 本 Lab 可與資安合規課並列；若學員無程式背景，允許純表格作業。

## 與 hexstrike_lab 對照

- 直接對應 `ExecutionOrchestrator.merge_into_report` 產生的 finding 結構；學員應能指出 **`evidence` vs `evidence_record`** 分工。

## 建議 Cursor 提示詞（分段給）

1. 「根據 hexstrike_lab 的 PENTEST_EVIDENCE_JSON_SCHEMA，列出我這份 log 缺哪些必填欄位。」
2. 「把下面自然語言步驟轉成 `tool.command` 陣列（假設路徑無空格）。」
