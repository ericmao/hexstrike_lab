# Lab 15 — 選修：雲端工具、Bug Bounty 規則、紫隊摘要，或 MCP × pipeline 橋接

**定位：** **選修模組**；依開課時數擇一或多個主題實作。與 [hexstrike-ai](https://github.com/0x4m4/hexstrike-ai) 能力清單對齊時需講師先行裁切工具範圍。

**Track C（P5 — AI for Red Team 自動化）：** 優先對照 **15D**（MCP × pipeline）；其餘小題見 [docs/TRACK_C_PENTEST.md](../../docs/TRACK_C_PENTEST.md)。

---

## 學習目標（擇一）

### 15A — 雲端／容器工具鏈（經 MCP）

- 在**授權雲實驗帳號**或**離線 mock**上，透過 MCP 觸發 **Prowler／Trivy／kube-bench** 等（以當日環境已安裝者為準）。
- 產出：發現摘要 + **RoE 合規檢查**（是否越權帳號）。

### 15B — Bug Bounty 規則演練

- 選一份**公開** Bug Bounty 計畫範圍（不含漏洞細節），讓 MCP 協助**製作檢核清單**：允許的測試類型、禁止的資料存取、報告格式。
- **不**對該程式實際送出任何測試流量，除非學員本人為合法參與者且講師同意。

### 15C — 紫隊（偵測視角）

- 從 Lab07–09 **任選一則**技術行為，撰寫 **Sigma／Splunk 偽語法** 或**一段 SOC 告警邏輯**（自然語言 + 欄位名即可）。
- 說明 **false positive** 來源。

### 15D — MCP × `hexstrike_lab pipeline` 橋接（進階）

- 設計（不必完整實作）一個流程：**MCP tool** 或 **shell 步驟**呼叫  
  `python -m hexstrike_lab pipeline --target ... --profile ...`  
  並將 `report.json` 路徑回傳給 LLM 做摘要。
- 討論 **timeout**、**路徑注入**、**profile 名稱白名單**。

## 授權與環境

- 依所選子題；預設 **15B 禁止實測**、**15A 僅實驗帳號**、**15C/D 僅本機與講義 log**。

## 操作步驟

由講師發放子題工作單；學員依子題完成**指定段落**與驗收。

## 驗收標準

- 提交：子題代號 + 產出物（清單／偵測草稿／設計圖）+ **50 字**反思。

## 講師提醒

- 本 Lab **不強制**全班同題；可分組。
- 15D 若實作，需 **code review** 防止 `subprocess` `shell=True` 與任意 profile 注入。

## 與 hexstrike_lab 對照

- 15D 直接整合本 repo CLI；15C 補足「只有掃描自動化不夠，還需**可觀測性**」。

## 建議 Cursor 提示詞（分段給）

- 15B：「只整理計畫文字中與『out of scope』相關的句子成表格，不要建議 exploit。」
- 15D：「畫出 MCP server 呼叫本機 CLI 的序列圖，標出信任邊界。」
