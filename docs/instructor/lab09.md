# Lab 09 — DVWA／授權 Web — 講師專用大綱

**學員教材：** [`labs/lab09/cursor_prompts.md`](../../labs/lab09/cursor_prompts.md)  
**回索引：** [`INSTRUCTOR_ANSWER_OUTLINE.md`](../INSTRUCTOR_ANSWER_OUTLINE.md)  
**Track C：** [`TRACK_C_PENTEST.md`](../TRACK_C_PENTEST.md) P2（Burp／raw request）

## 預期產物

- 講義聲明之 URL；sqlmap 或手動嘗試之 log。
- 變形 payload 列表；至少 2 失敗 + 1 成功或講師認可中止點。
- 倫理短文（約 200 字）。
- Track C：raw request 節錄（可遮罩 cookie）。

## 評分對照

| 等級 | 要點 |
|------|------|
| **及格** | 目標與講義一致；無越權 URL；有失敗軌跡。 |
| **優良** | 能解釋過濾與繞過邏輯與 sqlmap 參數取捨（risk／level）。 |

## 常見不合格徵兆

- 僅成功截圖無 log。
- Payload 明顯可套用到任意網站。

## 口試參考

- 在 Bug Bounty 計畫下，為何不宜「AI 全自動 sqlmap」？
