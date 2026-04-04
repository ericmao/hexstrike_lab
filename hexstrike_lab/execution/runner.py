from __future__ import annotations

import subprocess
import time
from typing import Any

from hexstrike_lab.execution.base import ToolAdapter, ToolResult


def _parsed_or_fallback(adapter: ToolAdapter, raw: ToolResult) -> dict[str, Any]:
    try:
        return adapter.normalize_result(raw)
    except Exception as exc:  # noqa: BLE001 — never fail the runner on parser bugs
        return {
            "schema": "hexstrike.adapter.v1",
            "adapter": adapter.name,
            "kind": "normalize_error",
            "message": str(exc),
        }


def run_adapter(
    adapter: ToolAdapter,
    target: str,
    *,
    options: dict[str, Any],
    timeout_sec: float,
    retries: int,
) -> ToolResult:
    """Run adapter with subprocess; capture stdout/stderr; optional retries on failure."""
    last_err: str | None = None
    norm_target = ""
    cmd: list[str] = []

    for attempt in range(max(1, retries + 1)):
        t0 = time.perf_counter()
        try:
            norm_target = adapter.validate_target(target)
            cmd = adapter.build_command(norm_target, options)
        except ValueError as e:
            return ToolResult(
                adapter=adapter.name,
                target=target,
                status="validation_error",
                exit_code=None,
                duration_ms=0.0,
                stdout="",
                stderr="",
                message=str(e),
                command=[],
                parsed={
                    "schema": "hexstrike.adapter.v1",
                    "adapter": adapter.name,
                    "kind": "validation_error",
                    "message": str(e),
                },
            )

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                check=False,
                shell=False,
            )
            dur = (time.perf_counter() - t0) * 1000
            raw = ToolResult(
                adapter=adapter.name,
                target=norm_target,
                status="ok" if proc.returncode == 0 else "error",
                exit_code=proc.returncode,
                duration_ms=dur,
                stdout=proc.stdout or "",
                stderr=proc.stderr or "",
                command=cmd,
            )
            raw.parsed = _parsed_or_fallback(adapter, raw)
            if raw.status == "ok" or attempt >= retries:
                return raw
            last_err = f"exit {proc.returncode}"
            time.sleep(min(2**attempt, 8.0))
        except OSError as e:
            dur = (time.perf_counter() - t0) * 1000
            raw = ToolResult(
                adapter=adapter.name,
                target=norm_target,
                status="error",
                exit_code=None,
                duration_ms=dur,
                stdout="",
                stderr="",
                message=f"Execution failed: {e}",
                command=cmd,
            )
            raw.parsed = _parsed_or_fallback(adapter, raw)
            return raw
        except subprocess.TimeoutExpired as e:
            dur = (time.perf_counter() - t0) * 1000
            out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
            err = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
            if attempt >= retries:
                raw = ToolResult(
                    adapter=adapter.name,
                    target=norm_target,
                    status="timeout",
                    exit_code=None,
                    duration_ms=dur,
                    stdout=out,
                    stderr=err,
                    message=f"Timeout after {timeout_sec}s",
                    command=cmd,
                )
                raw.parsed = _parsed_or_fallback(adapter, raw)
                return raw
            last_err = "timeout"
        time.sleep(min(2**attempt, 8.0))

    raw = ToolResult(
        adapter=adapter.name,
        target=target,
        status="error",
        exit_code=None,
        duration_ms=0.0,
        stdout="",
        stderr="",
        message=last_err or "retry exhausted",
        command=cmd,
    )
    raw.parsed = {
        "schema": "hexstrike.adapter.v1",
        "adapter": adapter.name,
        "kind": "retry_exhausted",
        "message": raw.message,
    }
    return raw
