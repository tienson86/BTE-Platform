"""Capture DU-01 live Cung Phi: Nam Khôn / Nữ Khảm → Tuyệt Mệnh."""

from __future__ import annotations

import json
import os
import socket
import subprocess
import sys
import time
from pathlib import Path
from urllib.request import Request, urlopen

from playwright.sync_api import Page, sync_playwright

from engines.calendar_engine.engine import CalendarEngine

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "docs" / "reports" / "tv01_marriage" / "du01"
SHOTS = OUT / "screenshots"
PORTAL_ROOT = REPO / "applications" / "customer_portal"
PORTAL = "http://127.0.0.1:8081"
MARRIAGE_API = "http://127.0.0.1:8082"


def _listen(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _kill_port(port: int) -> None:
    if os.name == "nt":
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
    deadline = time.time() + 10.0
    while time.time() < deadline and _listen(port):
        time.sleep(0.25)


def _spawn(app: str, port: int, factory: bool = False) -> None:
    args = [sys.executable, "-m", "uvicorn", app, "--host", "127.0.0.1", "--port", str(port)]
    if factory:
        args.append("--factory")
    log_path = OUT / f"uvicorn-{port}.log"
    log_path.parent.mkdir(parents=True, exist_ok=True)
    handle = log_path.open("ab")
    subprocess.Popen(args, cwd=str(REPO), stdout=handle, stderr=handle)


def _wait(port: int, timeout: float) -> None:
    deadline = time.time() + timeout
    while time.time() < deadline:
        if _listen(port):
            try:
                urlopen(f"http://127.0.0.1:{port}/healthz", timeout=2)
                return
            except Exception:
                try:
                    urlopen(f"http://127.0.0.1:{port}/marriage-consulting", timeout=2)
                    return
                except Exception:
                    pass
        time.sleep(0.25)
    raise RuntimeError(f"port {port} did not open")


def _cung_for(year: int, month: int, day: int, gender: str) -> str:
    """Read personal Cung Phi from CalendarEngine. Does not recalculate palaces in TV-01."""
    calendar = CalendarEngine().build(year, month, day, gender=gender)
    return str(calendar.cung_phi or "")


def _find_year(*, gender: str, palace: str) -> tuple[int, int, int]:
    """Find a civil date whose published personal Cung Phi matches palace."""
    engine = CalendarEngine()
    for year in range(1966, 2001):
        calendar = engine.build(year, 5, 15, gender=gender)
        if calendar.cung_phi == palace:
            return year, 5, 15
    raise RuntimeError(f"no_year_for:{gender}:{palace}")


def _iso(year: int, month: int, day: int) -> str:
    return f"{year:04d}-{month:02d}-{day:02d}"


def _display(year: int, month: int, day: int) -> str:
    return f"{day:02d}{month:02d}{year:04d}"


def _post(person_a: dict[str, str], person_b: dict[str, str]) -> dict[str, object]:
    body = {
        "person_a": person_a,
        "person_b": person_b,
        "options": {"language": "vi", "audience": "customer"},
    }
    request = Request(
        f"{MARRIAGE_API}/api/v1/consulting/marriage",
        data=json.dumps(body).encode("utf-8"),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        method="POST",
    )
    with urlopen(request, timeout=120) as response:
        return json.loads(response.read().decode("utf-8"))


def _report(consultation_id: str) -> dict[str, object]:
    request = Request(
        f"{MARRIAGE_API}/api/v1/consulting/marriage/{consultation_id}/report",
        headers={"Accept": "application/json"},
    )
    with urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def _relation(report: dict[str, object]) -> tuple[str, str, str]:
    sections = {item["section_id"]: item for item in (report.get("data") or {}).get("sections") or []}
    cung = sections.get("cung_phi") or {}
    blocks = {item["block_id"]: item for item in cung.get("blocks") or []}
    nam = str((blocks.get("cung-a") or {}).get("body") or "")
    nu = str((blocks.get("cung-b") or {}).get("body") or "")
    relation = str((blocks.get("cung-relation") or {}).get("body") or "")
    return nam, nu, relation


def _npm() -> str:
    return "npm.cmd" if os.name == "nt" else "npm"


def _fill(page: Page, *, a_date: str, b_date: str, a_name: str, b_name: str) -> None:
    page.fill("#person-a-full-name", a_name)
    page.check('input[name="person-a-gender"][value="male"]')
    page.fill("#person-a-birth-date", a_date)
    page.fill("#person-a-birth-time", "0730")
    page.fill("#person-a-birth-place", "Hà Nội")
    page.fill("#person-b-full-name", b_name)
    page.check('input[name="person-b-gender"][value="female"]')
    page.fill("#person-b-birth-date", b_date)
    page.fill("#person-b-birth-place", "Hà Nội")


def main() -> None:
    """Prove live TV-01 shows Tuyệt Mệnh for Nam Khôn / Nữ Khảm."""
    OUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    male_khon = (1987, 1, 21)
    assert _cung_for(*male_khon, "male") == "Khôn"
    female_kham = _find_year(gender="female", palace="Khảm")
    assert _cung_for(*female_kham, "female") == "Khảm"
    pairs = {
        "khon_kham": (
            {
                "full_name": "An",
                "gender": "male",
                "birth_date": _iso(*male_khon),
                "birth_time": "07:30",
                "birth_place": "Hà Nội",
            },
            {
                "full_name": "Lan",
                "gender": "female",
                "birth_date": _iso(*female_kham),
                "birth_place": "Hà Nội",
            },
            "Tuyệt Mệnh",
        ),
        "khon_can": (
            {
                "full_name": "An",
                "gender": "male",
                "birth_date": "1987-01-21",
                "birth_time": "07:30",
                "birth_place": "Hà Nội",
            },
            {
                "full_name": "Binh",
                "gender": "female",
                "birth_date": "1990-05-15",
                "birth_place": "Hà Nội",
            },
            "Sinh Khí",
        ),
    }
    subprocess.run([_npm(), "run", "build:result"], cwd=str(PORTAL_ROOT), check=True)
    _kill_port(8082)
    _spawn("consulting.marriage.api.http:create_marriage_api_app", 8082, factory=True)
    _wait(8082, 60.0)
    if _listen(8081):
        _kill_port(8081)
    _spawn("applications.customer_portal.app:app", 8081)
    _wait(8081, 30.0)
    live: dict[str, object] = {"female_kham_date": _iso(*female_kham), "pairs": {}}
    for key, (person_a, person_b, expected) in pairs.items():
        created = _post(person_a, person_b)
        consultation_id = str((created.get("data") or {}).get("consultation_id") or "")
        nam, nu, relation = _relation(_report(consultation_id))
        live["pairs"][key] = {
            "consultation_id": consultation_id,
            "nam": nam,
            "nu": nu,
            "relation": relation,
            "expected": expected,
        }
        if key == "khon_kham":
            assert nam == "Khôn" and nu == "Khảm"
            assert relation == "Tuyệt Mệnh"
            assert relation != "Ngũ Quỷ"
        else:
            assert relation == expected
    extra_female_ton = _find_year(gender="female", palace="Tốn")
    extra = _post(
        {
            "full_name": "Nam",
            "gender": "male",
            "birth_date": "1987-01-21",
            "birth_time": "07:30",
            "birth_place": "Hà Nội",
        },
        {
            "full_name": "Hong",
            "gender": "female",
            "birth_date": _iso(*extra_female_ton),
            "birth_place": "Hà Nội",
        },
    )
    extra_id = str((extra.get("data") or {}).get("consultation_id") or "")
    nam, nu, relation = _relation(_report(extra_id))
    live["pairs"]["khon_ton"] = {
        "consultation_id": extra_id,
        "nam": nam,
        "nu": nu,
        "relation": relation,
        "expected": "Thiên Y",
    }
    assert nam == "Khôn" and nu == "Tốn" and relation == "Thiên Y"
    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 1100})
        page.goto(f"{PORTAL}/marriage-consulting", wait_until="networkidle")
        page.wait_for_selector("#person-a-full-name")
        _fill(
            page,
            a_date=_display(*male_khon),
            b_date=_display(*female_kham),
            a_name="An",
            b_name="Lan",
        )
        page.click('[data-testid="submit-marriage"]')
        page.locator('[data-testid="marriage-result"]').wait_for(timeout=120000)
        page.locator('[data-testid="detailed-analysis"] > summary').click()
        page.locator('[data-testid="cung-phi"]').scroll_into_view_if_needed()
        page.locator('[data-testid="cung-phi"]').screenshot(path=str(SHOTS / "01_khon_kham_tuyet_menh.png"))
        visible = page.locator('[data-testid="cung-phi"]').inner_text()
        checks = {
            "live_khon_kham": live["pairs"]["khon_kham"]["relation"] == "Tuyệt Mệnh",
            "live_not_ngu_quy": live["pairs"]["khon_kham"]["relation"] != "Ngũ Quỷ",
            "ui_tuyet_menh": "Tuyệt Mệnh" in visible,
            "ui_not_ngu_quy": "Ngũ Quỷ" not in visible,
            "ui_khon": "Khôn" in visible,
            "ui_kham": "Khảm" in visible,
            "live_khon_can": live["pairs"]["khon_can"]["relation"] == "Sinh Khí",
            "live_khon_ton": live["pairs"]["khon_ton"]["relation"] == "Thiên Y",
        }
        browser.close()
    payload = {"status": "PASS" if all(checks.values()) else "FAIL", "checks": checks, "live": live}
    (OUT / "browser_verification.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    if payload["status"] != "PASS":
        raise RuntimeError(json.dumps(checks, ensure_ascii=False))


if __name__ == "__main__":
    main()
