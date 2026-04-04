# Lab 08 — 大量 JSON 報告分析與驗證節制

**對照講師手冊：** LAB3（Nuclei JSON、AI 協助驗證腳本）。**載體：** hexstrike-ai MCP + 本機工具鏈。

---

## 學習目標

- 對 **Nuclei（或課程指定）** 的 JSON 輸出做**分級、挑選 High/Critical、討論偽陽性**。
- 在**講師書面或口頭核准後**，才執行 AI 建議的 **Python 驗證腳本**（僅對靶機）。
- 以 **evidence 心智表**紀錄：工具、指令摘要、時間、target、核准人。

## 授權與環境

- 產生報告的 `-u` 或目標清單**僅限**講師提供之 URL／IP（例如 DVWA 或實驗用 VulnApp）。
- **課程環境變體：** 手冊中的 `/import lab3_report.json` 若不存在，改為「將檔案路徑貼入對話」或「由 MCP 讀檔」（依當日客戶端能力）。

## 操作步驟

1. 依講義執行（範例）：`nuclei -u http://&lt;靶機&gt; -j -o lab3_report.json`（參數以講師為準）。
2. 將 `lab3_report.json`（或摘要）交給 MCP 中的代理，要求：**分級統計、挑一則 High 說明理由、列出可能誤報原因**。
3. 下達（手冊意涵）：「為該 High 寫一支**最小** Python 驗證腳本，僅對上述 URL 發請求並印出關鍵回應片段。」
4. **Gate：** 講師簽名或群組頻道回覆「核准執行」後，學員才可 `python3 verify_vuln.py`。
5. 填寫 **evidence 心智表**（對齊本 repo `hexstrike.pentest_evidence.v1` 欄位意涵：adapter／command／status／parsed_summary 等）。

## 觀察／除錯

- 若腳本嘗試連線多個 host：**視為不合格**，需改寫。
- 討論：AI 產生的驗證碼是否可能**過度侵略**（大量請求、破壞資料）？

## 驗收標準

- 提交：`lab3_report.json`（或節錄）、驗證腳本、執行輸出、**evidence 心智表**、**核准紀錄**。
- 短文（200 字內）：此發現是**真陽性**或**需人工複核**的理由。

## 講師提醒

- **禁止**將真實客戶網站當作練習檔案來源。
- 若課程無 Nuclei，可改 **nikto／自訂 JSON**，但保留「大量結構化輸入 + 驗證節制」流程。

## 與 hexstrike_lab 對照

- `pipeline` 產出之 `report.json`／`parsed`：**規則化**；本 Lab 輸入來自 **第三方掃描器 JSON**，再由 LLM 解讀——思考如何未來用 **同一 evidence schema** 統一兩者。

## 建議 Cursor 提示詞（分段給）

1. 「請只分析 JSON 的 `info`／`severity` 分布，不要建議任何對外連線。」
2. 「把驗證腳本限制在單一 URL、單一 HTTP 方法、timeout 5 秒，並加上註解說明假設。」
