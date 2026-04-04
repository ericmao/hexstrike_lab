# Lab 14 — CI 與 Artifact Gate — 講師專用大綱

**學員教材：** [`labs/lab14/cursor_prompts.md`](../../labs/lab14/cursor_prompts.md)  
**回索引：** [`INSTRUCTOR_ANSWER_OUTLINE.md`](../INSTRUCTOR_ANSWER_OUTLINE.md)

## 預期產物

- CI 設定檔（或本機 `act` 等同物）與一次 **green run** 證明。
- `pipeline` **dry-run**（無 `--execute`）+ 對 `report.json` 之 schema 驗證步驟。
- 約 100 字：dry-run gate 對教學與迴歸的意義。

## 評分對照

| 等級 | 要點 |
|------|------|
| **及格** | CI 內未對真實目標 `--execute`；使用 documentation IP 或講師約定離線策略。 |
| **優良** | 處理 `run_id` 變動（找最新 `report.json` 之腳本或策略有文件化）。 |

## 常見不合格徵兆

- 硬編碼過期 `run_id` 導致下次 PR 失敗卻無說明。
- 僅跑 pytest 未驗證 scan document schema。

## 口試參考

- MCP 路線要做類似 gate，多卡在哪一層（mock？成本？）？
