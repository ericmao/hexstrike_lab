# Lab 05 — 滲測工作流與證據 — 講師專用大綱

**學員教材：** [`labs/lab05/cursor_prompts.md`](../../labs/lab05/cursor_prompts.md)  
**回索引：** [`INSTRUCTOR_ANSWER_OUTLINE.md`](../INSTRUCTOR_ANSWER_OUTLINE.md)

## 預期產物

- 多步**滲測式**工作流（階段、決策點）。
- 證據輸出設計或與 `evidence_record`／`pentest_workflow` 意涵對齊之欄位表。

## 評分對照

| 等級 | 要點 |
|------|------|
| **及格** | 與 `pentest_workflow.yaml`、`evidence_schema` 概念一致，非口號。 |
| **優良** | 能對照 Lab13：指出哪些欄位在真實 MCP 流程易缺漏。 |

## 常見不合格徵兆

- 工作流無授權／範圍節點。
- 證據僅「截圖一堆」無結構化欄位意識。

## 口試參考

- `evidence_record` 最少要留住哪幾類資訊才足以給第三方稽核？
