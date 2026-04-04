# Lab 11 — 綜合黑箱／CTF 與滲透報告

**對照講師手冊：** LAB6（Phase 1–3 全週期 + `/generate_report`）。**載體：** hexstrike-ai MCP。

---

## 學習目標

- 在**全新靶機 IP**（講師發放）上，依 **Phase 1→2→3** 自主完成：服務發現、弱點檢索與利用敘述、權限提升敘述（深度依課程時數調整）。
- 產出 **Markdown 滲透報告**（手冊的 `/generate_report --format markdown` 若不可用，則由 MCP 對話生成或 Cursor 匯出）。
- 另交 **半頁對照**：同一標的用 **`hexstrike_lab pipeline`**（任一 profile）跑出的 **JSON／manifest** 與本 Lab **質性報告**的差異。

### Track C 加強（P4 — Attack chain）

- 報告內必含 **foothold → 提權或橫向（擇一）→ 影響** 的 **三格表**（每格 1–2 句 + 證據指到 log／截圖）。
- （選）**MITRE ATT&CK** 技術 ID **至少 2 個**對照到上述階段。
- （選）若靶場提供 **flag／objective**：列入驗收；否則以講師簽字之「中止點分析」替代。

## 授權與環境

- 靶機僅限講師於實驗室內提供之 IP；**禁止**學員自帶目標。
- Phase 內容**難度**由講師預先驗證（Jenkins／Redis 等僅為手冊舉例，實際以當期靶場為準）。

## 操作步驟

1. **Phase 1：** 發現非預期服務或高風險埠；記錄指令與證據。
2. **Phase 2：** 請代理**檢索**該服務的已知漏洞類型（**文獻級**，不要求自動 exploit 除非課程允許）。
3. **Phase 3：** 依講義完成利用與提權**敘述**（若時數不足，改為「計畫書 + 風險評級」）。
4. 產出 Markdown 報告：需含**執行摘要、範圍、方法、發現、嚴重度、建議、授權聲明**。
5. 於本 repo 根目錄執行：  
   `python -m hexstrike_lab pipeline --target <同一IP> --profile quick --output-base output`（dry-run 可接受，但需說明）。

## 觀察／除錯

- 代理是否**幻覺**未執行的步驟？報告須附**可對應的 log 或輸出**。
- 比較：`pipeline` 的 **機械式 findings** 與 CTF **敘述式**報告的讀者分別是誰？

## 驗收標準

- Markdown 報告一份 + **hexstrike_lab** 產物路徑截圖（`report.json` 或 `manifest.json`）+ **半頁對照文** + **Track C 三格 attack-chain 表**（及選修 flag／ATT&CK）。
- 口試：若客戶只要「合規掃描證據」，你會交哪一份產出？

## 講師提醒

- 本 Lab **最易超時**；可提供「完成 Phase 1–2 即及格」的梯度假分級。
- 強調：**報告中的授權聲明**為必填段落。

## 與 hexstrike_lab 對照

| hexstrike_lab pipeline | 本 Lab（MCP + 人類敘述） |
|------------------------|---------------------------|
| schema、manifest、可重現步驟 | 故事線、風險脈絡、修補建議 |
| 適合 CI／稽核附檔 | 適合人讀的交付 |

## 建議 Cursor 提示詞（分段給）

1. 「先只產出報告大綱與每節需要的證據清單，不要寫內文。」
2. 「把 Phase 2 的『CVE 檢索』限制在 2020 年後、且與我們掃到的版本字串相符的條目。」
