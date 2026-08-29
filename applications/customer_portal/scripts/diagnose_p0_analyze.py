"""P0 diagnose Analyze submit: console, network, validation."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "knowledge" / "commercial_dashboard" / "implementation" / "p0_analyze"
API_PORT = 8000
PORTAL_PORT = 8081
BASE = f"http://127.0.0.1:{PORTAL_PORT}"


def _listening(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _kill_port(port: int) -> None:
    if os.name == "nt":
        lookup = subprocess.run(
            ["netstat", "-ano"],
            capture_output=True,
            text=True,
            check=False,
        )
        pids: set[str] = set()
        for line in lookup.stdout.splitlines():
            if f":{port} " not in line or "LISTENING" not in line.upper():
                continue
            pid = line.split()[-1]
            if pid.isdigit() and pid != "0":
                pids.add(pid)
        for pid in pids:
            subprocess.run(["taskkill", "/PID", pid, "/F"], capture_output=True, check=False)
    deadline = time.time() + 5
    while time.time() < deadline and _listening(port):
        time.sleep(0.2)


def _spawn(module: str, port: int) -> subprocess.Popen[bytes]:
    env = os.environ.copy()
    env["BTE_API_BASE_URL"] = f"http://127.0.0.1:{API_PORT}"
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            module,
            "--host",
            "127.0.0.1",
            "--port",
            str(port),
        ],
        cwd=str(REPO),
        env=env,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def _wait(port: int, timeout: float = 20.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api_proc = _spawn("applications.api.app:app", API_PORT)
    portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    logs: list[dict[str, object]] = []
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            page = browser.new_page(viewport={"width": 1280, "height": 900}, locale="en-US")
            page.on("console", lambda msg: logs.append({"type": "console", "level": msg.type, "text": msg.text}))
            page.on("pageerror", lambda err: logs.append({"type": "pageerror", "text": str(err)}))
            page.on(
                "request",
                lambda req: logs.append({"type": "request", "method": req.method, "url": req.url})
                if "/analyze" in req.url or "/backend" in req.url
                else None,
            )
            page.on(
                "response",
                lambda res: logs.append({"type": "response", "status": res.status, "url": res.url})
                if "/analyze" in res.url or "/backend" in res.url
                else None,
            )
            page.on("requestfailed", lambda req: logs.append({"type": "requestfailed", "url": req.url, "error": req.failure}))
            page.goto(f"{BASE}/analyze", wait_until="networkidle")
            page.fill("#full_name", "Nguyen Tien Son")
            page.check("#gender_male")
            page.fill("#birth_date", "21/01/1987")
            page.fill("#birth_time", "04:30")
            page.fill("#birth_place", "Ha Tay, Viet Nam")
            state = page.evaluate(
                """() => ({
                  date: document.getElementById('birth_date').value,
                  time: document.getElementById('birth_time').value,
                  gender: document.querySelector('input[name=gender]:checked') && document.querySelector('input[name=gender]:checked').value,
                  hasPortal: Boolean(window.BtePortal),
                  hasPost: Boolean(window.BtePortal && window.BtePortal.post),
                  hasStore: Boolean(window.BtePortal && window.BtePortal.ResultStore),
                  parse: (function(){
                    var raw = document.getElementById('birth_date').value;
                    var m = raw.match(/^(\\d{1,2})\\/(\\d{1,2})\\/(\\d{4})$/);
                    return { raw: raw, match: m && m.slice(0,4) };
                  })()
                })"""
            )
            logs.append({"type": "preclick_state", **state})
            page.click("#btnAnalyze")
            try:
                page.wait_for_url("**/result", timeout=120000)
                logs.append({"type": "redirect", "url": page.url})
            except Exception as exc:
                logs.append(
                    {
                        "type": "no_redirect",
                        "url": page.url,
                        "error": str(exc),
                        "flash": page.locator("#globalFlash").inner_text(),
                        "date_err": page.locator("#err_birth_date").inner_text(),
                        "status": page.locator("#analyzeStatus").inner_text(),
                    }
                )
            page.screenshot(path=str(OUT / "runtime.png"), full_page=True)
            browser.close()
    finally:
        (OUT / "devtools.json").write_text(json.dumps(logs, ensure_ascii=True, indent=2), encoding="utf-8")
        print("wrote", OUT / "devtools.json")
        for proc in (portal_proc, api_proc):
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    main()
