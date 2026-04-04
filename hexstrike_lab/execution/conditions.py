from __future__ import annotations

from typing import Any


def _last_step_for_adapter(
    prior_steps: list[dict[str, Any]],
    adapter: str,
) -> dict[str, Any] | None:
    for step in reversed(prior_steps):
        if step.get("adapter") == adapter:
            return step
    return None


def evaluate_run_when(
    run_when: dict[str, Any] | None,
    prior_steps: list[dict[str, Any]],
    *,
    dry_run: bool,
) -> tuple[bool, str | None]:
    """Decide whether a conditional step should run.

    If ``run_when`` is omitted or empty, the step always runs.

    Supported shape (extensible for future labs)::

        run_when:
          after_adapter: nmap
          open_ports_any_of: [80, 443, 8080]

    In dry-run mode, conditions are not evaluated against real scan data; all
    steps are planned so operators see the full workflow.
    """
    if not run_when:
        return True, None
    if not isinstance(run_when, dict):
        raise ValueError("run_when must be a mapping when present")
    if dry_run:
        return True, None

    after = run_when.get("after_adapter")
    ports_any = run_when.get("open_ports_any_of")
    if after is None or ports_any is None:
        raise ValueError("run_when requires 'after_adapter' and 'open_ports_any_of'")

    ref = _last_step_for_adapter(prior_steps, str(after))
    if ref is None:
        return False, f"no prior step for adapter {after!r}"

    status = ref.get("status")
    if status != "ok":
        return False, f"prior {after} status was {status!r} (need ok)"

    parsed = ref.get("parsed") if isinstance(ref.get("parsed"), dict) else {}
    data = parsed.get("data") if isinstance(parsed.get("data"), dict) else {}
    open_ports = data.get("open_ports")
    if not isinstance(open_ports, list):
        return False, f"prior {after} has no parsed.data.open_ports list"

    want = {int(p) for p in ports_any}
    got: set[int] = set()
    for entry in open_ports:
        if isinstance(entry, dict) and "port" in entry:
            try:
                got.add(int(entry["port"]))
            except (TypeError, ValueError):
                continue

    if got & want:
        return True, None
    return False, f"no open port in {sorted(want)} (got {sorted(got)})"
