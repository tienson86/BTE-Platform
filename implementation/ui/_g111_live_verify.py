"""G1-11 live: rebuild result bundle, restart runtime, Analyze 1966, screenshot header."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
API_PORT = 8000
PORTAL_PORT = 8081
LOCAL = f"http://localhost:{PORTAL_PORT}"
PY = REPO / ".venv" / "Scripts" / "python.exe"
if not PY.exists():
    PY = Path(sys.executable)
NPM = "npm.cmd" if os.name == "nt" else "npm"


def listening(port: int) -> bool:
    sock = socket.socket()
    sock.settimeout(0.4)
    try:
        return sock.connect_ex(("127.0.0.1", port)) == 0
    finally:
        sock.close()


def kill_port(port: int) -> None:
    lookup = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, check=False)
    pids: set[str] = set()
    for line in lookup.stdout.splitlines():
        if f":{port} " not in line or "LISTENING" not in line.upper():
            continue
        pid = line.split()[-1]
        if pid.isdigit() and pid != "0":
            pids.add(pid)
    for pid in pids:
        subprocess.run(["taskkill", "/PID", pid, "/F"], capture_output=True, check=False)
    deadline = time.time() + 8
    while time.time() < deadline and listening(port):
        time.sleep(0.2)


def spawn(module: str, port: int) -> subprocess.Popen[bytes]:
    env = os.environ.copy()
    env["BTE_API_BASE_URL"] = f"http://127.0.0.1:{API_PORT}"
    log = OUT / f"_uvicorn_{port}.log"
    handle = log.open("wb")
    return subprocess.Popen(
        [
            str(PY),
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
        stdout=handle,
        stderr=subprocess.STDOUT,
    )


def wait_port(port: int, timeout: float = 45.0) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if listening(port):
            return
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def analyze_http() -> dict:
    body = json.dumps(
        {
            "year": 1966,
            "month": 9,
            "day": 24,
            "hour": 4,
            "minute": 15,
            "gender": "male",
            "full_name": "G1-11 live",
            "birth_place": "Ha Noi",
        }
    ).encode("utf-8")
    req = urllib.request.Request(
        f"{LOCAL}/backend/api/v1/analyze",
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=90) as res:
        return json.loads(res.read().decode("utf-8"))


def main() -> None:
    lines: list[str] = []
    portal_dir = REPO / "applications" / "customer_portal"
    build = subprocess.run(
        [NPM, "run", "build:result"],
        cwd=str(portal_dir),
        capture_output=True,
        text=True,
        check=False,
    )
    lines.append(f"build:result exit={build.returncode}")
    if build.returncode != 0:
        lines.append(build.stdout[-800:] + build.stderr[-800:])
        (OUT / "_g111_live.txt").write_text("\n".join(lines), encoding="utf-8")
        raise SystemExit(build.returncode)

    kill_port(API_PORT)
    kill_port(PORTAL_PORT)
    lines.append(f"ports_free 8000={not listening(8000)} 8081={not listening(8081)}")
    api_proc = spawn("applications.api.app:app", API_PORT)
    portal_proc = spawn("applications.customer_portal.app:app", PORTAL_PORT)
    wait_port(API_PORT)
    wait_port(PORTAL_PORT)
    lines.append(f"spawned api_pid={api_proc.pid} portal_pid={portal_proc.pid}")

    http = analyze_http()
    data = http.get("data") or {}
    cx = data.get("can_xuong") or {}
    ident_bw = ((data.get("identity") or {}).get("bone_weight") or {})
    lines.append("HTTP can_xuong=" + json.dumps(cx, ensure_ascii=False))
    lines.append("HTTP identity.bone_weight=" + json.dumps(ident_bw, ensure_ascii=False))
    lines.append(f"HTTP year={((data.get('bazi') or {}).get('year_pillar') or {}).get('stem')}")

    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1648, "height": 928})
        page = context.new_page()
        page.goto(f"{LOCAL}/result", wait_until="domcontentloaded", timeout=60000)
        page.evaluate(
            """() => {
              ['bte_last_result','bte_current_analysis_id','bte_view_result'].forEach((key) => {
                localStorage.removeItem(key);
                sessionStorage.removeItem(key);
              });
            }"""
        )
        page.goto(f"{LOCAL}/analyze", wait_until="networkidle", timeout=60000)
        page.fill("#full_name", "G1-11 live")
        page.check("#gender_male")
        page.fill("#birth_date", "24/09/1966")
        page.fill("#birth_time", "04:15")
        page.fill("#birth_place", "Hà Nội")
        page.click("#btnAnalyze")
        page.wait_for_url("**/result", timeout=120000)
        page.wait_for_selector("[data-identity-header='true']", timeout=30000)
        page.wait_for_timeout(600)

        stored = page.evaluate(
            """() => sessionStorage.getItem('bte_last_result') || localStorage.getItem('bte_last_result')"""
        )
        stored_cx = {}
        if stored:
            try:
                payload = json.loads(stored)
                stored_cx = (payload.get("data") or {}).get("can_xuong") or {}
            except json.JSONDecodeError:
                stored_cx = {"error": "unreadable"}
        lines.append("STORE can_xuong=" + json.dumps(stored_cx, ensure_ascii=False))

        header = page.evaluate(
            """() => {
              const header = document.querySelector('[data-identity-header=true]');
              const cx = document.querySelector('[data-module=bone-weight]');
              const tutru = document.querySelector('[data-testid=tu-tru-panel]');
              const tech = document.querySelector('[data-region=status]');
              const id = document.querySelector('[data-slot=analysis-id]');
              const scripts = [...document.querySelectorAll('script[src]')].map((el) => el.src);
              return {
                href: location.href,
                scripts,
                cxText: cx ? cx.innerText : '',
                tutru: tutru ? tutru.innerText.replace(/\\s+/g, ' ').trim() : '',
                tech: tech ? tech.innerText.replace(/\\s+/g, ' ').trim() : '',
                analysisIdWrap: id ? getComputedStyle(id).whiteSpace : '',
                headerHeight: header ? header.getBoundingClientRect().height : 0,
              };
            }"""
        )
        lines.append("DOM=" + json.dumps(header, ensure_ascii=False))
        page.screenshot(path=str(OUT / "G1_11_localhost_result_header.png"), full_page=False)
        page.locator("[data-identity-header='true']").screenshot(
            path=str(OUT / "G1_11_localhost_header_card.png")
        )
        if page.query_selector("#sec-can-xuong"):
            page.locator("#sec-can-xuong").screenshot(path=str(OUT / "G1_11_localhost_can_xuong_detail.png"))
        browser.close()

    (OUT / "_g111_live.txt").write_text("\n".join(lines), encoding="utf-8")
    print("WROTE", OUT / "_g111_live.txt")


if __name__ == "__main__":
    main()
