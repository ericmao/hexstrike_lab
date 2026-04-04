# Lab 10 — 程式修補與 JSON — 講師專用大綱

**學員教材：** [`labs/lab10/cursor_prompts.md`](../../labs/lab10/cursor_prompts.md)  
**回索引：** [`INSTRUCTOR_ANSWER_OUTLINE.md`](../INSTRUCTOR_ANSWER_OUTLINE.md)  
**Track C：** [`TRACK_C_PENTEST.md`](../TRACK_C_PENTEST.md) P3

## 預期產物

- Python 3 可執行碼；**單一 JSON 物件**範例輸出。
- （選）反彈 shell：僅講師核准 + 隔離網之 listener 證據。
- Track C：簡短 bypass／編碼思路敘述（不對非授權標的實測）。

## 評分對照

| 等級 | 要點 |
|------|------|
| **及格** | 無未審查之 `eval`／危險 `os.system`；JSON 欄位符合講義。 |
| **優良** | 程式碼審查過程有逐段註記或對照 `hexstrike_lab` 之 subprocess 安全慣例。 |

## 常見不合格徵兆

- AI 全文重寫但學員無法解釋任一行。
- shell 選修在未簽核下出現公網 listener。

## 口試參考

- 為何不能把「改 exploit」全權交給 AI？

## 講師備註

- 預設評分以程式品質與審查為主；**不強制** shell 成功。
