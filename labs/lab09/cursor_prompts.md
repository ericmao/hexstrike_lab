# Lab 09 — 授權 Web 靶機：弱點與繞過（DVWA 等）

**對照講師手冊：** LAB4（DVWA Medium、SQLi 變形、sqlmap tamper）。**載體：** hexstrike-ai MCP。

---

## 學習目標

- 在 **DVWA Security Level = Medium**（或講師指定級別）下，理解**過濾與繞過**概念。
- 透過代理協助產生 **payload 變形**思路與 **sqlmap** 參數建議（**僅針對講義 URL**）。
- 記錄**失敗嘗試**與**成功條件**，避免只有「結果截圖」。

## 授權與環境

- **唯一允許**的 SQLi 頁面 URL 須印於講義首頁（例如 `http://192.168.56.101/vulnerabilities/sqli/`）。
- **嚴禁**對非靶機、非該路徑執行 sqlmap 或手動注入。

## 操作步驟

1. 登入 DVWA，確認 Security Level。
2. 提示代理：單引號被過濾情境下，請給 **5 個**不同編碼／變形思路（**不**要求直接給 exploit 外洩真實站）。
3. 請代理建議 **sqlmap** 指令，含 **tamper** 概念；由學員在**核准終端**執行，並保存完整 log。
4. 實驗紀錄須含：**至少 2 次失敗**與 **1 次成功或講師認定之中止點**（時間不夠時以分析代替成功）。

## 觀察／除錯

- 討論：為何在真實 Bug Bounty 中「請 AI 自動 sqlmap」可能**違反計畫規則**？
- 觀察代理是否建議**過寬**的 `--risk`／`--level`；講師應要求降級參數。

## 驗收標準

- 提交：URL 聲明、sqlmap（或手動）log 節錄、變形 payload 列表、**200 字倫理反思**（授權測試 vs 任意測試）。

## 講師提醒

- 本 Lab **必念**：未授權測試違法／違規；本堂僅限實驗室 DVWA。
- 若學員心理壓力大，可提供「純閱讀 log + 不改參數」的替代驗收（講師事前公告）。

## 與 hexstrike_lab 對照

- 本 repo **不包含** sqlmap 適配器；思考若要以 **ToolAdapter** 包 sqlmap，**validate_target** 應如何**白名單化**。

## 建議 Cursor 提示詞（分段給）

1. 「在不產生實際請求的前提下，解釋 Medium 級別 DVWA 可能如何過濾單引號。」
2. 「列出 sqlmap 的 `charencode` tamper 用途與風險（對目標負載與日誌）。」
