"""TV1-B07B reproduction: live portal submit + network/log capture.

Does not start 8082. Records where the live request chain stops.
"""

from __future__ import annotations

import json
import socket
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

REPO = Path(__file__).resolve().parents[3]
OUT = REPO / "docs" / "reports" / "tv01_marriage" / "b07b"
SHOTS = OUT / "screenshots"
PORTAL = "http://127.0.0.1:8081"
PROXY_URL = f"{PORTAL}/backend/api/v1/consulting/marriage"
DIRECT_URL = "http://127.0.0.1:8082/api/v1/consulting/marriage"
SAMPLE = {
    "person_a": {
        "full_name": "An",
        "gender": "male",
        "birth_date": "1987-01-21",
        "birth_time": "07:30",
        "birth_place": {"display_name": "Hà Nội"},
    },
    "person_b": {
        "full_name": "Binh",
        "gender": "female",
        "birth_date": "1990-05-15",
        "birth_place": {"display_name": "Hà Nội"},
    },
    "options": {"language": "vi", "audience": "customer", "expert_mode": False},
}


def _listen(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.settimeout(0.4)
        return sock.connect_ex(("127.0.0.1", port)) == 0


def _http(method: str, url: str, body: dict | None = None, timeout: float = 8.0) -> dict:
    data = None if body is None else json.dumps(body).encode("utf-8")
    headers = {"Accept": "application/json"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    request = urllib.request.Request(url, data=data, headers=headers, method=method)
    started = time.perf_counter()
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read().decode("utf-8", "replace")
            return {
                "url": url,
                "method": method,
                "status": int(getattr(response, "status", 200) or 200),
                "duration_ms": round((time.perf_counter() - started) * 1000, 1),
                "body": raw[:4000],
            }
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode("utf-8", "replace")
        return {
            "url": url,
            "method": method,
            "status": int(exc.code),
            "duration_ms": round((time.perf_counter() - started) * 1000, 1),
            "body": raw[:4000],
        }
    except Exception as exc:
        return {
            "url": url,
            "method": method,
            "status": None,
            "duration_ms": round((time.perf_counter() - started) * 1000, 1),
            "error": f"{type(exc).__name__}: {exc}",
        }


def main() -> None:
    """Reproduce the live stall and write evidence."""
    OUT.mkdir(parents=True, exist_ok=True)
    SHOTS.mkdir(parents=True, exist_ok=True)
    evidence: dict[str, object] = {
        "ports": {
            "8081": _listen(8081),
            "8082": _listen(8082),
            "8000": _listen(8000),
            "80": _listen(80),
        }
    }
    evidence["direct_8082_get"] = _http("GET", "http://127.0.0.1:8082/api/v1/consulting/marriage")
    evidence["direct_8082_post"] = _http("POST", DIRECT_URL, SAMPLE)
    evidence["proxy_post"] = _http("POST", PROXY_URL, SAMPLE)
    evidence["wrong_port80_post"] = _http(
        "POST",
        "http://127.0.0.1/backend/api/v1/consulting/marriage",
        SAMPLE,
        timeout=5.0,
    )

    with sync_playwright() as playwright:
        browser = playwright.chromium.launch()
        page = browser.new_page(viewport={"width": 1440, "height": 900})
        requests: list[dict[str, object]] = []

        def on_request(request) -> None:
            if "consulting/marriage" in request.url or "backend" in request.url:
                requests.append(
                    {
                        "phase": "request",
                        "url": request.url,
                        "method": request.method,
                        "headers": dict(request.headers),
                        "post_data": request.post_data,
                    }
                )

        def on_response(response) -> None:
            if "consulting/marriage" in response.url or "/backend/" in response.url:
                body = ""
                try:
                    body = response.text()[:2000]
                except Exception:
                    body = "<unreadable>"
                requests.append(
                    {
                        "phase": "response",
                        "url": response.url,
                        "status": response.status,
                        "body": body,
                    }
                )

        page.on("request", on_request)
        page.on("response", on_response)
        console: list[str] = []
        page.on("console", lambda msg: console.append(f"{msg.type}: {msg.text}"))
        page.on("pageerror", lambda err: console.append(f"pageerror: {err}"))

        page.goto(f"{PORTAL}/marriage-consulting", wait_until="networkidle")
        page.wait_for_selector("#marriage-consulting-root")
        page.wait_for_selector("#person-a-full-name")
        page.fill("#person-a-full-name", "An")
        page.check('input[name="person-a-gender"][value="male"]')
        page.fill("#person-a-birth-date", "21011987")
        page.fill("#person-a-birth-time", "0730")
        page.fill("#person-a-birth-place", "Hà Nội")
        page.fill("#person-b-full-name", "Binh")
        page.check('input[name="person-b-gender"][value="female"]')
        page.fill("#person-b-birth-date", "15051990")
        page.fill("#person-b-birth-place", "Hà Nội")
        page.click('[data-testid="submit-marriage"]')
        page.wait_for_timeout(8000)
        loading = page.locator('[data-testid="loading-state"]').count()
        error = page.locator('[data-testid="error-state"]').count()
        result = page.locator('[data-testid="marriage-result"]').count()
        page.screenshot(path=str(SHOTS / "00_repro_after_submit.png"), full_page=True)
        evidence["browser"] = {
            "requests": requests,
            "console": console,
            "loading": loading,
            "error": error,
            "result": result,
            "loading_text": page.locator('[data-testid="loading-state"]').inner_text()
            if loading
            else None,
            "error_text": page.locator('[data-testid="error-state"]').inner_text() if error else None,
        }
        browser.close()

    (OUT / "repro_evidence.json").write_text(
        json.dumps(evidence, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({"ports": evidence["ports"], "browser": evidence["browser"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
