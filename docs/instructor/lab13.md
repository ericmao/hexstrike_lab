# Lab 13 — 證據鏈對照 `evidence_record` — 講師專用大綱

**學員教材：** [`labs/lab13/cursor_prompts.md`](../../labs/lab13/cursor_prompts.md)  
**回索引：** [`INSTRUCTOR_ANSWER_OUTLINE.md`](../INSTRUCTOR_ANSWER_OUTLINE.md)

## 預期產物

- **同一授權事件**之雙表述：MCP／工具脈絡 + 對齊 `hexstrike.pentest_evidence.v1` 之表格或 JSON 草稿。
- 200 字：若送稽核，會補哪三個欄位？

## 評分對照

| 等級 | 要點 |
|------|------|
| **及格** | 欄位與 [`evidence_schema.py`](../../hexstrike_lab/core/evidence_schema.py) 意涵大致對齊；指出 MCP 易缺欄位。 |
| **優良** | 時間線 T0／T1／T2 與欄位 `collected_at`／`workflow_step_id` 呼應。 |

## 常見不合格徵兆

- 兩種表述實際為不同事件。
- `command` argv 無法還原卻未討論改善。

## 口試參考

- 若 argv 從證據中消失，稽核或鑑識會面臨什麼問題？
