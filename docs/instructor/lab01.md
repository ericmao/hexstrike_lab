# Lab 01 — Adapter — 講師專用大綱

**學員教材：** [`labs/lab01/cursor_prompts.md`](../../labs/lab01/cursor_prompts.md)  
**回索引：** [`INSTRUCTOR_ANSWER_OUTLINE.md`](../INSTRUCTOR_ANSWER_OUTLINE.md)

## 預期產物

- `ToolAdapter` 概念實作或設計：安全執行（避免 `shell=True`）、JSON 輸出、錯誤處理。
- normalize：工具 stdout → 結構化 JSON 的範例或程式片段。

## 評分對照

| 等級 | 要點 |
|------|------|
| **及格** | 與 `run_adapter` 契約一致；失敗時有結構化錯誤，非僅裸 traceback。 |
| **優良** | 具 `validate_target` 或等效白名單；能說明為何拒絕某類字元。 |

## 常見不合格徵兆

- 建議或實作 `shell=True` 而未討論風險。
- 輸出非 JSON 或可解析結構，無 schema 意識。

## 口試參考

- 為何 subprocess 列表參數比單一字串 shell 安全？
