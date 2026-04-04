# hexstrike_lab

**僅供授權內部實驗室使用。** 本專案是一套輕量、模組化的 **安全測試自動化** 框架：**占位掃描器**、以 **profile** 驅動的 **`nmap` / `nikto`** 執行、可選的 **條件式步驟**、正規化 **JSON** 報告、**Markdown** 摘要，以及受控流程用的 **證據紀錄（evidence_record）**。

僅在您擁有或取得 **明確書面授權** 的系統上使用。本專案 **不包含** 漏洞利用模組。

**其他語言：** [English README](README.md)

---

## 目錄

- [套件內容](#套件內容)
- [環境需求](#環境需求)
- [安裝與設定](#安裝與設定)
- [從專案根目錄執行](#從專案根目錄執行)
- [指令說明](#指令說明)
- [Profile 一覽](#profile-一覽)
- [設定檔說明](#設定檔說明)
- [Pipeline 輸出目錄結構](#pipeline-輸出目錄結構)
- [RFP 與滲測工作流文件](#rfp-與滲測工作流文件)
- [實驗與教材](#實驗與教材)
- [延伸文件](#延伸文件)
- [測試](#測試)
- [授權與法律聲明](#授權與法律聲明)

---

## 套件內容

| 區域 | 說明 |
|------|------|
| `hexstrike_lab/cli/` | 命令列：`run`、`assess`、`pipeline`、`report` |
| `hexstrike_lab/scanners/` | 行程內 **占位** 掃描器（供 `run` 使用） |
| `hexstrike_lab/adapters/` + `execution/` | **ToolAdapter**：`subprocess`、驗證、正規化 `parsed` JSON |
| `hexstrike_lab/pipeline/` | 完整流程：原始輸出、`report.json`、`summary.md`、manifest、CTI stub |
| `hexstrike_lab/reports/` | JSON → Markdown（`generate_markdown_report`） |
| `configs/` | `default.yaml`、`profiles.yaml`、RFP／滲測工作流 YAML |
| `labs/` | 各實驗的 Cursor 提示片段 |
| `docs/` | Runbook、執行層說明、Cursor 提示包、講師指南 |

執行層細節請見 [docs/EXECUTION_LAYER.md](docs/EXECUTION_LAYER.md)。

---

## 環境需求

- **Python 3.10+**（建議 3.10；CI 可能使用更新版本）
- 使用 `assess` / `pipeline` 並加上 **`--execute`** 做**真實掃描**時：系統 `PATH` 需有 **`nmap`**、**`nikto`**
- 工具安裝以 **Kali** 或其他 Debian 系為常見選擇

---

## 安裝與設定

### 複製儲存庫

```bash
git clone https://github.com/ericmao/hexstrike_lab.git
cd hexstrike_lab
```

### 虛擬環境（建議）

```bash
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 選用：Kali 套件

```bash
sudo apt update
sudo apt install -y python3 python3-venv python3-pip make
# 真實掃描時：
sudo apt install -y nmap nikto
```

更完整的 Kali 說明見 [docs/RUNBOOK_KALI.md](docs/RUNBOOK_KALI.md)。

---

## 從專案根目錄執行

指令預設在**目前工作目錄**含有 **`configs/`** 的情況下執行（通常即儲存庫根目錄）。

```bash
cd hexstrike_lab
python -m hexstrike_lab --help
python -m hexstrike_lab <command> --help
```

---

## 指令說明

### `run`：占位掃描器

執行內建、**不呼叫外部安全工具**的占位掃描器，於 stdout 輸出一份 **符合 schema** 的 JSON。

```bash
python -m hexstrike_lab run --target 127.0.0.1 --pretty
```

| 參數 | 說明 |
|------|------|
| `--target` | 主機名稱或 IP（實驗目標） |
| `--config` | YAML 路徑（預設：`configs/default.yaml`） |
| `--pretty` | 縮排 JSON |

---

### `assess`：依 profile 執行工具

從 `configs/profiles.yaml` 載入 **profile**，執行 **nmap**／**nikto** 步驟；**預設為 dry-run**（僅輸出計畫中的指令列，不實際執行工具），除非加上 **`--execute`**。

```bash
# 安全：只印出計畫中的參數列
python -m hexstrike_lab assess --target 192.0.2.1 --profile quick --pretty

# 真實執行：需 nmap / nikto 在 PATH
python -m hexstrike_lab assess --target 192.0.2.1 --profile web --execute --pretty
```

| 參數 | 說明 |
|------|------|
| `--target` | 實驗室主機或 IP |
| `--profile` | 見下方 [Profile 一覽](#profile-一覽) |
| `--config` | 基礎設定（預設：`configs/default.yaml`） |
| `--profiles` | Profile 檔（預設：`configs/profiles.yaml`） |
| `--execute` | 實際執行外部工具 |
| `--pretty` | 縮排 JSON |

輸出為單一 JSON：`orchestration`、`findings`，工具相關 finding 可含 **`evidence_record`** 等欄位。

---

### `pipeline`：端到端產物

編排邏輯與 `assess` 相同，並將結果寫入 **`--output-base`** 底下（預設 `output/`）。

```bash
python -m hexstrike_lab pipeline --target 192.0.2.1 --profile quick --output-base output
python -m hexstrike_lab pipeline --target 192.0.2.1 --profile web --output-base output --execute
```

| 參數 | 說明 |
|------|------|
| `--target` | 實驗室主機或 IP |
| `--profile` | Profile 名稱 |
| `--output-base` | `raw/`、`json/`、`reports/`、`integration/` 的根目錄 |
| `--config` / `--profiles` | 同 `assess` |
| `--execute` | 真實掃描；未指定時仍為 dry-run，但**仍會寫出產物** |

**Shell 輔助腳本**（若存在 `.venv/bin/python` 會優先使用）：

```bash
chmod +x scripts/run_full_pipeline.sh
./scripts/run_full_pipeline.sh 192.0.2.1 quick
./scripts/run_full_pipeline.sh 192.0.2.1 web --execute
```

---

### `report`：從 JSON 產生 Markdown

由既有的 **`report.json`**（通過 schema 驗證）重新產生摘要 Markdown。

```bash
python -m hexstrike_lab report from-json --input output/json/<run_id>/report.json --output recap.md
python -m hexstrike_lab report from-json --input output/json/<run_id>/report.json   # 輸出至 stdout
```

---

## Profile 一覽

定義於 **`configs/profiles.yaml`**。以下名稱皆可用於 `assess` 與 `pipeline` 的 `--profile`。

| Profile | 用途簡述 |
|---------|-----------|
| `quick` | 精簡 nmap |
| `web` | nmap（網頁埠）+ nikto |
| `full` | 較廣 nmap + nikto |
| `adaptive_web` | nmap 後，**僅在**常見網頁埠開放時執行 nikto（`run_when`） |
| `rfp_automated_scan` | 貼近 RFP 的埠集合 + 條件式 nikto；對照 `configs/rfp_scan_requirements.yaml` |
| `pentest_lab` | 多步驟：偵查 → 列舉 → 條件式 web；含 **`evidence_record`** 用中繼資料；對照 `configs/pentest_workflow.yaml` |

請依實驗室環境調整 YAML 中的逾時、重試與 `options`。

---

## 設定檔說明

| 檔案 | 用途 |
|------|------|
| `configs/default.yaml` | 實驗室中繼資料、日誌、輸出 schema 版本 |
| `configs/profiles.yaml` | Profile 定義（`steps`、`adapter`、`run_when`、`pentest_phase` 等） |
| `configs/rfp_scan_requirements.yaml` | RFP 需求與流程之對應（可追溯性） |
| `configs/pentest_workflow.yaml` | 滲測階段設計與綁定之 profile |

---

## Pipeline 輸出目錄結構

執行 `pipeline` 後，每次 run 會有一個 UTC 時間戳 **`run_id`**（例如 `20260404_123456`）。

```
output/
├── raw/<run_id>/           # step_00_nmap.txt 等（stdout／stderr／command）
├── json/<run_id>/
│   ├── report.json         # 完整掃描文件
│   └── manifest.json       # 階段、計數、路徑
├── reports/<run_id>/
│   └── summary.md          # 可讀摘要
└── integration/
    └── cti_export_<run_id>.ndjson
```

stdout 另會印出含 `status`、`run_id`、`paths` 的小型 JSON。

---

## RFP 與滲測工作流文件

- **RFP 掃描**：`configs/rfp_scan_requirements.yaml` 將需求編號對應到工具與產物；profile 為 `rfp_automated_scan`。
- **實驗室滲測式工作流**：`configs/pentest_workflow.yaml` 描述階段與決策點；profile 為 `pentest_lab`。
- 程式載入（供工具／測試）：`hexstrike_lab.core.rfp_workflow`、`hexstrike_lab.core.pentest_workflow`。

---

## 實驗與教材

雙軌說明見 [`labs/README.md`](labs/README.md)：

- **Track A（lab00 … lab05）：** 建構並使用**本儲存庫**之 `hexstrike_lab`（CLI、適配器、Pipeline、RFP／滲測 YAML、證據）。
- **Track B（lab06 … lab15）：** 外部 **[hexstrike-ai](https://github.com/0x4m4/hexstrike-ai)** MCP 與授權實驗情境、RoE、證據對照、CI gate、選修。**本 repo 未內嵌**該專案；若課程使用自訂 HexStrike CLI，請以各 `labs/labNN/cursor_prompts.md` 的 **課程環境變體**為準。

核心文件：

- **`docs/CURSOR_PROMPT_PACK.md`** — Track A 階段 + Track B 表與短提示。
- **`docs/INSTRUCTOR_PROMPT_GUIDE.md`** — 何時給提示；Lab08–11 **安全 gate**。

---

## 延伸文件

- [docs/RUNBOOK_KALI.md](docs/RUNBOOK_KALI.md) — Kali 安裝與範例
- [docs/EXECUTION_LAYER.md](docs/EXECUTION_LAYER.md) — 適配器、安全預設、擴充點
- [SECURITY.md](SECURITY.md) — 負責任使用說明

---

## 測試

```bash
make test
# 或
python -m pytest tests/ -v
```

Makefile 捷徑：

```bash
make run          # 占位 run
make assess-dry   # dry-run assess（quick profile）
make pipeline-dry # dry-run pipeline，輸出至 ./output
```

---

## 授權與法律聲明

Copyright © 2026 **ACTC** — *International Information Security Talent Cultivation and Promotion Association*（國際資訊安全人才培育與推廣協會）.  
本專案以 [MIT License](LICENSE) 授權。

**法律聲明：** 僅在您擁有或取得明確書面授權的系統上使用。本軟體不提供任何保證；您須自行遵守適用法令與組織政策。
