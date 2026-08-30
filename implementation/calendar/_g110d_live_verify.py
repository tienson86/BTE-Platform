"""G1-10D live runtime: restart servers, Analyze 1966, screenshot localhost /result."""

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
LOOPBACK = f"http://127.0.0.1:{PORTAL_PORT}"
PY = REPO / ".venv" / "Scripts" / "python.exe"
if not PY.exists():
    PY = Path(sys.executable)


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


def wait_port(port: int, timeout: float = 40.0) -> None:
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
            "full_name": "G1-10D live",
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


def storage_dump(page) -> dict[str, str]:
    return page.evaluate(
        """() => {
          const keys = ['bte_last_result','bte_current_analysis_id','bte_history','bte_view_result'];
          const read = (store) => {
            const out = {};
            keys.forEach((key) => { out[key] = store.getItem(key); });
            return out;
          };
          return { origin: location.origin, local: read(localStorage), session: read(sessionStorage) };
        }"""
    )


def pillar_cung(raw: str | None, which: str) -> str:
    if not raw:
        return ""
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError:
        return "unreadable"
    data = payload.get("data") if isinstance(payload, dict) else {}
    ident = ((data or {}).get("identity") or {}).get("four_pillars") or {}
    bazi = (data or {}).get("bazi") or {}
    cell = ident.get(which) or {}
    pillar = bazi.get(f"{which}_pillar") or {}
    return f"ident={cell.get('cung_phi')} bazi={pillar.get('cung_phi')} ver={(data or {}).get('calendar', {}).get('calendar_rule_version')}"


def main() -> None:
    lines: list[str] = []
    kill_port(API_PORT)
    kill_port(PORTAL_PORT)
    lines.append(f"ports_free 8000={not listening(8000)} 8081={not listening(8081)}")
    api_proc = spawn("applications.api.app:app", API_PORT)
    portal_proc = spawn("applications.customer_portal.app:app", PORTAL_PORT)
    wait_port(API_PORT, 45)
    wait_port(PORTAL_PORT, 45)
    lines.append(f"spawned api_pid={api_proc.pid} portal_pid={portal_proc.pid}")

    http = analyze_http()
    data = http.get("data") or {}
    cal = data.get("calendar") or {}
    ident = (data.get("identity") or {}).get("four_pillars") or {}
    bazi = data.get("bazi") or {}
    lines.append(f"HTTP calendar_rule_version={cal.get('calendar_rule_version')}")
    lines.append(f"HTTP tam_nguyen={cal.get('tam_nguyen')}")
    for key in ("year", "month", "day", "hour"):
        cell = ident.get(key) or {}
        pillar = bazi.get(f"{key}_pillar") or {}
        lines.append(
            f"HTTP {key} {cell.get('can_chi')} ident={cell.get('cung_phi')} bazi={pillar.get('cung_phi')} src={pillar.get('source_nguyen')}"
        )

    analyze_body: dict | None = None
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 1100})
        page = context.new_page()
        page.on(
            "response",
            lambda res: res.url.endswith("/api/v1/analyze") and res.request.method == "POST",
        )

        def grab_analyze(response) -> None:
            nonlocal analyze_body
            if "/api/v1/analyze" in response.url and response.request.method == "POST":
                try:
                    analyze_body = response.json()
                except Exception:
                    analyze_body = None

        page.on("response", grab_analyze)

        page.goto(f"{LOOPBACK}/result", wait_until="domcontentloaded", timeout=60000)
        loop_before = storage_dump(page)
        lines.append("127 origin before=" + json.dumps(loop_before, ensure_ascii=False)[:800])

        page.goto(f"{LOCAL}/result", wait_until="domcontentloaded", timeout=60000)
        local_before = storage_dump(page)
        lines.append("localhost origin before=" + json.dumps(local_before, ensure_ascii=False)[:800])

        page.evaluate(
            """() => {
              ['bte_last_result','bte_current_analysis_id','bte_view_result'].forEach((key) => {
                localStorage.removeItem(key);
                sessionStorage.removeItem(key);
              });
            }"""
        )

        page.goto(f"{LOCAL}/analyze", wait_until="networkidle", timeout=60000)
        page.fill("#full_name", "G1-10D live")
        page.check("#gender_male")
        page.fill("#birth_date", "24/09/1966")
        page.fill("#birth_time", "04:15")
        page.fill("#birth_place", "Hà Nội")
        page.click("#btnAnalyze")
        page.wait_for_url("**/result", timeout=120000)
        page.wait_for_selector("[data-testid='tu-tru-panel']", timeout=30000)
        page.wait_for_timeout(800)

        stored = storage_dump(page)
        last = (stored.get("session") or {}).get("bte_last_result") or (stored.get("local") or {}).get(
            "bte_last_result"
        )
        lines.append("localhost after save year=" + pillar_cung(last, "year"))
        lines.append("localhost after save month=" + pillar_cung(last, "month"))
        lines.append("loaded id=" + str((stored.get("session") or {}).get("bte_current_analysis_id")))

        rows = page.evaluate(
            """() => {
              const panel = document.querySelector('[data-testid=tu-tru-panel]');
              const out = {};
              ['year','month','day','hour'].forEach((key) => {
                const row = panel && panel.querySelector('[data-pillar=\"' + key + '\"]');
                out[key] = row ? row.innerText.replace(/\\s+/g, ' ').trim() : '';
              });
              const scripts = [...document.scripts].map((s) => s.src).filter(Boolean);
              return { rows: out, scripts, href: location.href };
            }"""
        )
        lines.append("DOM=" + json.dumps(rows, ensure_ascii=False))
        shot = OUT / "G1_10D_localhost_result_tutru.png"
        page.locator("[data-region='pillars']").screenshot(path=str(shot))
        page.screenshot(path=str(OUT / "G1_10D_localhost_result_full.png"), full_page=True)
        lines.append(f"screenshot={shot}")

        page.goto(f"{LOCAL}/good-date", wait_until="networkidle", timeout=60000)
        home = page.evaluate(
            """async () => {
              const res = await fetch('/backend/api/v1/date-selection/day', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({year: 1966, month: 9, day: 24})
              });
              const json = await res.json();
              const day = json.data || {};
              const hour = (day.hours || []).find((item) => (item.window || {}).branch === 'Dần') || {};
              if (window.BteTuTruPanel) {
                window.BteTuTruPanel.mount(document.getElementById('dsTuTru'), {
                  year: { canChi: (day.year || {}).can_chi, napAm: (day.year || {}).nayin_element, cungPhi: (day.year || {}).cung_phi },
                  month: { canChi: (day.month || {}).can_chi, napAm: (day.month || {}).nayin_element, cungPhi: (day.month || {}).cung_phi },
                  day: { canChi: (day.day || {}).can_chi, napAm: (day.day || {}).nayin_element, cungPhi: (day.day || {}).cung_phi },
                  hour: { canChi: hour.can_chi || hour.ganzhi, napAm: hour.nayin_element || hour.nayin, cungPhi: hour.cung_phi || hour.cung }
                });
              }
              const panel = document.querySelector('#dsTuTru [data-testid=tu-tru-panel]');
              const text = panel ? panel.innerText.replace(/\\s+/g, ' ').trim() : '';
              return {
                year: (day.year || {}).cung_phi,
                month: (day.month || {}).cung_phi,
                day: (day.day || {}).cung_phi,
                hour: hour.cung_phi || hour.cung,
                dom: text
              };
            }"""
        )
        lines.append("homepage=" + json.dumps(home, ensure_ascii=False))
        page.locator("#dsTuTru").screenshot(path=str(OUT / "G1_10D_localhost_homepage_tutru.png"))
        browser.close()

    if analyze_body:
        cal2 = (analyze_body.get("data") or {}).get("calendar") or {}
        lines.append(f"browser Analyze version={cal2.get('calendar_rule_version')} tam={cal2.get('tam_nguyen')}")

    (OUT / "_g110d_live.txt").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines[-20:]))


if __name__ == "__main__":
    main()
