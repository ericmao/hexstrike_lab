from __future__ import annotations

import subprocess
from unittest.mock import patch

from hexstrike_lab.adapters.nmap import NmapAdapter
from hexstrike_lab.adapters.nikto import NiktoAdapter
from hexstrike_lab.adapters.text_parsers import parse_nikto_stdout, parse_nmap_stdout
from hexstrike_lab.execution.base import ToolResult
from hexstrike_lab.execution.runner import run_adapter


def test_parse_nmap_stdout_extracts_open_ports():
    text = """
PORT     STATE SERVICE VERSION
22/tcp   open  ssh     OpenSSH 8.0
80/tcp   open  http    Apache
443/tcp  open  https
""".strip()
    out = parse_nmap_stdout(text)
    assert out["open_count"] == 3
    assert out["open_ports"][0]["port"] == 22
    assert out["open_ports"][0]["service"] == "ssh"
    assert out["open_ports"][1]["protocol"] == "tcp"


def test_parse_nikto_stdout_collects_plus_lines():
    text = """
+ Target: https://example/
+ Server: nginx
- scan done
""".strip()
    out = parse_nikto_stdout(text)
    assert "Target:" in out["findings"][0]
    assert out["finding_count"] == 2


def test_nmap_adapter_normalize_includes_schema_and_data():
    raw = ToolResult(
        adapter="nmap",
        target="192.0.2.1",
        status="ok",
        exit_code=0,
        duration_ms=1.0,
        stdout="22/tcp   open  ssh     OpenSSH\n",
        stderr="",
        command=["nmap", "192.0.2.1"],
    )
    p = NmapAdapter().normalize_result(raw)
    assert p["schema"] == "hexstrike.adapter.v1"
    assert p["data"]["open_count"] == 1
    assert p["run"]["status"] == "ok"


def test_run_adapter_oserror_returns_structured_parsed():
    adapter = NmapAdapter()
    with patch("hexstrike_lab.execution.runner.subprocess.run") as run:
        run.side_effect = FileNotFoundError("nmap")
        res = run_adapter(
            adapter,
            "192.0.2.1",
            options={"ports": "80"},
            timeout_sec=5.0,
            retries=0,
        )
    assert res.status == "error"
    assert "Execution failed" in (res.message or "")
    assert res.parsed.get("schema") == "hexstrike.adapter.v1"
    assert "data" in res.parsed


def test_run_adapter_timeout_still_populates_parsed():
    adapter = NiktoAdapter()

    def _timeout(*_a: object, **_kw: object) -> None:
        raise subprocess.TimeoutExpired(cmd=["nikto"], timeout=0.01, output="+ scan line\n")

    with patch("hexstrike_lab.execution.runner.subprocess.run", side_effect=_timeout):
        res = run_adapter(
            adapter,
            "192.0.2.1",
            options={"ssl": False, "port": 80, "maxtime_sec": 1},
            timeout_sec=0.01,
            retries=0,
        )
    assert res.status == "timeout"
    assert res.parsed.get("schema") == "hexstrike.adapter.v1"
    assert res.parsed.get("adapter") == "nikto"
