from hexstrike_lab.pipeline.runner import precheck_environment


def test_precheck_execute_warns_without_tools(monkeypatch):
    monkeypatch.setattr("hexstrike_lab.pipeline.runner.shutil.which", lambda _: None)
    w = precheck_environment(execute=True)
    assert any("nmap" in x for x in w)
    assert any("nikto" in x for x in w)


def test_precheck_dry_run_skips_tool_checks(monkeypatch):
    monkeypatch.setattr("hexstrike_lab.pipeline.runner.shutil.which", lambda _: None)
    w = precheck_environment(execute=False)
    assert not any("nmap" in x for x in w)
    assert not any("nikto" in x for x in w)
