# Claude Code（Kali）— hexstrike-ai MCP JSON 範例

對應拓樸說明見 [TOPOLOGY_192.168.1.203_NDR.md](TOPOLOGY_192.168.1.203_NDR.md)（**標的 192.168.1.203**、中間 **NDR bridge**）。  
上游專案：[hexstrike-ai](https://github.com/0x4m4/hexstrike-ai) — 檔名與參數以你 clone 的 commit／講義為準。

---

## 設定檔位置（Claude Code）

- **使用者層級（常見）：** `~/.claude.json` 內的 **`mcpServers`** 物件。  
- **專案層級：** 專案目錄下的 **`.mcp.json`**（若你的 Claude Code 版本支援）。  
- 若檔案已存在其他 MCP，請**合併** `mcpServers` 的 key，勿整檔覆蓋。

官方文件會更新，請交叉比對：[Claude Code MCP](https://docs.claude.com/en/docs/claude-code/mcp)。

---

## 範例片段（stdio → 本機 hexstrike_server）

後端與 MCP 橋接都在 **同一台 Kali** 時，`--server` 使用 **loopback**；**不要**把標的 `192.168.1.203` 寫進 `--server`。

請將路徑改成你機器上的**絕對路徑**（venv 目錄名依上游 README 可能為 `hexstrike-env` 或其他）。

完整可複製範本見：[claude_code_mcp_hexstrike.example.json](claude_code_mcp_hexstrike.example.json)

```json
{
  "mcpServers": {
    "hexstrike-ai": {
      "command": "/home/kali/hexstrike-ai/hexstrike-env/bin/python3",
      "args": [
        "/home/kali/hexstrike-ai/hexstrike_mcp.py",
        "--server",
        "http://127.0.0.1:8888"
      ]
    }
  }
}
```

### 啟動順序建議

1. Kali 上先啟動：`python3 hexstrike_server.py`（或講義指定之綁定與埠，**需監聽 127.0.0.1 或 0.0.0.0**）。  
2. `curl -s http://127.0.0.1:8888/health` 成功後再開 Claude Code。  
3. （選）Ollama 依上游說明接在 hexstrike 設定，**非**本 JSON 必填欄位。

---

## 後端跑在「另一台主機」時

若 `hexstrike_server` 在實驗室內 **192.168.1.x** 的另一台 VM（**不是** 192.168.1.203 靶機，除非講師明定）：

```json
"args": [
  "/home/kali/hexstrike-ai/hexstrike_mcp.py",
  "--server",
  "http://192.168.1.50:8888"
]
```

將 `192.168.1.50` 換成實際伺服器 IP；防火牆需允許 Kali → 該 IP:8888。

---

## CLI 等效（可選）

若偏好指令註冊 MCP（版本需支援）：

```bash
claude mcp add --transport stdio hexstrike-ai -- /home/kali/hexstrike-ai/hexstrike-env/bin/python3 /home/kali/hexstrike-ai/hexstrike_mcp.py --server http://127.0.0.1:8888
```

---

## 與「標的 192.168.1.203」的關係

- **MCP JSON：** 只負責 **Claude ↔ hexstrike-ai 後端** 的控制通道。  
- **192.168.1.203：** 在 **Lab07+** 或講師核准之提示詞／工具參數中作為**白名單目標**；經 **NDR bridge** 時仍為一般 IP 連線。  
- 學員繳交之連線圖應**同時**畫出上述兩條邏輯（控制平面 vs 授權測試目標）。

---

## Claude Desktop（非 Code）對照

macOS 常見路徑：`~/Library/Application Support/Claude/claude_desktop_config.json`，`mcpServers` 結構類似；Kali 上若無 Desktop 可略過。
