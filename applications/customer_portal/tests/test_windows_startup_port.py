"""Windows launcher contracts for the primary local portal."""

from __future__ import annotations

from pathlib import Path

from applications.customer_portal.config import settings


REPO_ROOT = Path(__file__).resolve().parents[3]
WINDOWS_DEPLOYMENT = REPO_ROOT / "deployment" / "windows"


def test_windows_portal_launcher_uses_primary_port_8686() -> None:
    source = (WINDOWS_DEPLOYMENT / "start_portal.bat").read_text(encoding="utf-8")
    assert "set DEFAULT_PORT=8686" in source
    assert "set DEFAULT_PORT=8081" not in source
    assert "set DEFAULT_PORT=8083" not in source


def test_windows_startup_summary_reports_primary_port_8686() -> None:
    source = (WINDOWS_DEPLOYMENT / "start_all.bat").read_text(encoding="utf-8")
    assert "Portal   http://127.0.0.1:8686" in source


def test_windows_stop_script_does_not_depend_on_process_inventory_tools() -> None:
    source = (WINDOWS_DEPLOYMENT / "stop_all.bat").read_text(encoding="utf-8")
    assert "for %%R in (8000 8080 8081 8082 8686)" in source
    assert "netstat -ano" in source
    assert "Get-CimInstance" not in source
    assert "wmic process" not in source.lower()


def test_all_primary_local_launchers_use_port_8686() -> None:
    assert settings.port == 8686
    assert '"port": 8686' in (REPO_ROOT / "configs" / "services.json").read_text(
        encoding="utf-8"
    )
    assert 'PORTAL_URL = "http://localhost:8686"' in (
        REPO_ROOT / "runtime" / "manager.py"
    ).read_text(encoding="utf-8")
    assert 'DEFAULT_PORTAL_URL = "http://localhost:8686"' in (
        REPO_ROOT / "launcher" / "open_browser.py"
    ).read_text(encoding="utf-8")
    for environment in ("development.env", "production.env"):
        source = (REPO_ROOT / "deployment" / "env" / environment).read_text(
            encoding="utf-8"
        )
        assert "PORTAL_PORT=8686" in source
