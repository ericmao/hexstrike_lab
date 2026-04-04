# Lab 02 — Orchestrator — 講師專用大綱

**學員教材：** [`labs/lab02/cursor_prompts.md`](../../labs/lab02/cursor_prompts.md)  
**回索引：** [`INSTRUCTOR_ANSWER_OUTLINE.md`](../INSTRUCTOR_ANSWER_OUTLINE.md)

## 預期產物

- 編排邏輯說明（何時執行哪一步）。
- 與 profile／步驟條件（如 `run_when` 意涵）相連的設計敘述或簡圖。

## 評分對照

| 等級 | 要點 |
|------|------|
| **及格** | 規則式「下一步」可描述，非僅線性腳本順序。 |
| **優良** | 能舉例「前一步失敗則跳過／降級」並對應到資料欄位。 |

## 常見不合格徵兆

- 只有偽碼無對應到本 repo 的 orchestration 概念。
- 與 Lab01 適配器責任邊界不清。

## 口試參考

- `run_when` 與「由 LLM 決定下一步」在可稽核性上的根本差異？
