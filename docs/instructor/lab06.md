# Lab 06 — MCP 與 hexstrike-ai 後端 — 講師專用大綱

**學員教材：** [`labs/lab06/cursor_prompts.md`](../../labs/lab06/cursor_prompts.md)  
**回索引：** [`INSTRUCTOR_ANSWER_OUTLINE.md`](../INSTRUCTOR_ANSWER_OUTLINE.md)

## 參考範例（repo 內）

- Claude Code MCP JSON、**192.168.1.203 + NDR bridge** 拓樸說明：[`labs/lab06/examples/`](../../labs/lab06/examples/CLAUDE_CODE_MCP_JSON.md)

## 預期產物

- 連線示意圖（Client → MCP → HTTP server →（選）Ollama）。
- `health` 成功之截圖或 log；Ollama／`llama3` 依講義之 `ollama list` 與推論節錄。
- 各元件責任之短文說明。

## 評分對照

| 等級 | 要點 |
|------|------|
| **及格** | 層次正確；IP／埠／路徑可與截圖對讀。 |
| **優良** | 能說明**課程環境變體**（自訂 CLI vs 上游 MCP）下同等驗收如何取代。 |

## 常見不合格徵兆

- 將 `python -m hexstrike_lab` 誤稱為 MCP。
- 僅有 UI 截圖無法對應實際 listening 位址。

## 口試參考

- stdio MCP 與 HTTP server 各解決哪一類整合問題？
