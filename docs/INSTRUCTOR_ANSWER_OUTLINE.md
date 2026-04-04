# 講師專用 — 解答大綱與評分對照（索引）

**閱讀對象：** 講師與助教。**不建議**原封不動發給學員當「標準答案」；滲透相關以**驗收產物 + 口試**為主。

---

## 逐課大綱（一課一檔）

請使用 **[`docs/instructor/README.md`](instructor/README.md)** 目錄索引，或直接開啟：

- [Lab 00](instructor/lab00.md) · [Lab 01](instructor/lab01.md) · [Lab 02](instructor/lab02.md) · [Lab 03](instructor/lab03.md) · [Lab 04](instructor/lab04.md) · [Lab 05](instructor/lab05.md)
- [Lab 06](instructor/lab06.md) · [Lab 07](instructor/lab07.md) · [Lab 08](instructor/lab08.md) · [Lab 09](instructor/lab09.md) · [Lab 10](instructor/lab10.md) · [Lab 11](instructor/lab11.md)
- [Lab 12](instructor/lab12.md) · [Lab 13](instructor/lab13.md) · [Lab 14](instructor/lab14.md) · [Lab 15](instructor/lab15.md)

**學員操作步驟與提示：** 各課 [`labs/labNN/cursor_prompts.md`](../labs/README.md)

**其他講師文件：** [INSTRUCTOR_PROMPT_GUIDE.md](INSTRUCTOR_PROMPT_GUIDE.md) · [TRACK_C_PENTEST.md](TRACK_C_PENTEST.md)

---

## 評分原則（全課適用）

| 維度 | 及格（Pass） | 優良（Distinction） |
|------|----------------|----------------------|
| **範圍** | 產物與講義白名單一致，無「順手多掃」敘述 | 主動標註邊界與假設，能說明為何不敢越界 |
| **可稽核** | log／截圖／檔案路徑能對上文字陳述 | 時間線清楚，指令 argv 可追溯 |
| **治理** | RoE／核准 gate 有遵守（Lab08–11） | 能對照真實專案中誰該簽字、如何存證 |
| **AI 使用** | 能說明何時用 AI、何時必須人工 | 能指出 AI 幻覺或過度侵略建議並糾正 |

**Track A 客觀對照：** `pytest` 通過與 schema／CLI 行為；講師仍可要求口試解釋設計取捨。

---

## 快速檢核表（講師課末用）

- [ ] Lab08：是否有**書面／頻道核准**再跑驗證腳本？
- [ ] Lab09–11：目標是否**僅**講師發放？
- [ ] Lab11：報告是否**每節**指到 log／檔案？
- [ ] Lab12–13：是否至少考一題**口試**？
- [ ] Track A 作業：`pytest` 是否綠燈（若適用）？

---

## 版本與免責

本大綱隨 repo 教材更新；**實際授權與法遵**以各校與客戶合約為準。滲透相關敘述僅供**已授權實驗室教學**使用。
