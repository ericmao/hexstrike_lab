from __future__ import annotations

import subprocess
import time
from typing import Any

from hexstrike_lab.execution.base import ToolAdapter, ToolResult


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
            )

        try:
            proc = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout_sec,
                check=False,
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
            raw.parsed = adapter.normalize_result(raw)
            if raw.status == "ok" or attempt >= retries:
                return raw
            last_err = f"exit {proc.returncode}"
            time.sleep(min(2**attempt, 8.0))
        except subprocess.TimeoutExpired as e:
            dur = (time.perf_counter() - t0) * 1000
            out = e.stdout.decode() if isinstance(e.stdout, bytes) else (e.stdout or "")
            err = e.stderr.decode() if isinstance(e.stderr, bytes) else (e.stderr or "")
            if attempt >= retries:
                return ToolResult(
                    adapter=adapter.name,
                    target=norm_target,
                    status="timeout",
                    exit_code=None,
                    duration_ms=dur,
                    stdout=out,
                    stderr=err,
                    message=f"Timeout after {timeout_sec}s",
                    command=cmd,
                    parsed={},
                )
            last_err = "timeout"
        time.sleep(min(2**attempt, 8.0))

    return ToolResult(
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
