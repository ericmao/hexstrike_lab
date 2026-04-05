# Lab 07 — 結構化偵察 — 講師專用大綱

**學員教材：** [`labs/lab07/cursor_prompts.md`](../../labs/lab07/cursor_prompts.md)  
**回索引：** [`INSTRUCTOR_ANSWER_OUTLINE.md`](../INSTRUCTOR_ANSWER_OUTLINE.md)  
**Track C：** 見 [`TRACK_C_PENTEST.md`](../TRACK_C_PENTEST.md) P1

**參考範例（實測 + 範例繳交稿，標的 `192.168.1.203`）：** [`labs/lab07/examples/README.md`](../../labs/lab07/examples/README.md)

## 預期產物

- 掃描摘要表（白名單內目標）。
- **至少一條完整 argv 溯源**（來自 server log 或工具原始輸出）。
- 簡答：LLM 選工具 vs `run_when` 規則。

## 評分對照

| 等級 | 要點 |
|------|------|
| **及格** | 表內目標均在講義白名單；溯源非純模型口述。 |
| **優良** | Track C：AI 草擬策略 + **人工刪減後**可執行指令之對照。 |

## 常見不合格徵兆

- 無法指出實際執行的 `nmap`（或等效）參數列。
- 表內出現未授權網段。

## 口試參考

- 若模型宣稱掃描某 IP，你如何向稽核證明「真的執行過」？
