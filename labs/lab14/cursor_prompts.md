# Lab 14 — 自動化與 CI：dry-run、Schema 與 Artifact Gate

**定位：** 延伸 Track A；可在**無 MCP** 或 **CI 容器**內完成。

---

## 學習目標

- 在 **CI**（GitHub Actions、GitLab CI 或本機 `act`）中執行 **`hexstrike_lab pipeline` dry-run**，將產物當作 **artifact** 或僅驗證 **exit code**。
- 撰寫一步驟：對 `report.json` 執行 **schema 驗證**（可呼叫 `python -c` 引用 `validate_scan_document`）。
- 解釋為何 **dry-run** 仍對教學與「配置迴歸」有價值。

## 授權與環境

- CI 中**不**對真實網路目標執行 `--execute`；僅 `192.0.2.1` 等 **Documentation IP** 或講師提供的 **offline** 模式。
- 產物目錄使用 `output_ci/` 避免與本機混淆。

## 操作步驟

1. 新增或修改 workflow：checkout → setup Python → `pip install -r requirements.txt` → `python -m hexstrike_lab pipeline --target 192.0.2.1 --profile quick --output-base output_ci`（**勿**加 `--execute`）。
2. 加一步：`python -c "import json; from hexstrike_lab.core.schema import validate_scan_document; validate_scan_document(json.load(open('output_ci/json/.../report.json')))"`（路徑可用 `find` 或講師固定 `run_id` 策略；實作時可改為腳本搜最新子目錄）。
3. （選）上傳 `manifest.json` 為 artifact。
4. 文件化：若 PR 改壞 `profiles.yaml`，CI 如何**第一時間**發現？

## 觀察／除錯

- `run_id` 目錄每次不同：討論用 **固定 symlink** 或 **小腳本**找最新 `json/*/report.json`。
- MCP 路線能否做類似 gate？（通常需 mock server，進階選修。）

## 驗收標準

- 提交：CI 設定檔連結或附檔 + 一次 **green run** 截圖 + **100 字**說明 dry-run gate 的意義。

## 講師提醒

- 注意 **CI 分鐘數**與 **artifact 儲存成本**；可僅驗證 schema 不上傳 raw。

## 與 hexstrike_lab 對照

- 直接使用 [`hexstrike_lab/pipeline/runner.py`](../../hexstrike_lab/pipeline/runner.py) 行為；與 Lab06–11 **互補**（自動化 vs 人機 MCP）。

## 建議 Cursor 提示詞（分段給）

1. 「寫一個 bash 一行指令，在 output_ci/json 下找最新的 report.json 路徑。」
2. 「若 validate_scan_document 失敗，如何在 GitHub Actions 裡印出 JSON 路徑與第一個驗證錯誤？」
