"""Live process restart probe (API only). Not a Linux container substitute."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PORT = int(os.environ.get("BTE_G3_02_RESTART_PORT", "18000"))
HOST = "127.0.0.1"


def _wait_health(timeout: float = 30.0) -> dict:
    url = f"http://{HOST}:{PORT}/health"
    deadline = time.time() + timeout
    last = ""
    while time.time() < deadline:
        try:
            with urllib.request.urlopen(url, timeout=2) as response:
                return json.loads(response.read().decode("utf-8"))
        except (urllib.error.URLError, TimeoutError, ConnectionError) as exc:
            last = str(exc)
            time.sleep(0.4)
    raise RuntimeError(f"health timeout: {last}")


def _analyze() -> dict:
    body = json.dumps(
        {
            "year": 1985,
            "month": 9,
            "day": 18,
            "hour": 8,
            "minute": 0,
            "gender": "male",
            "timezone": "Asia/Bangkok",
            "full_name": "Ngo Dac Dung",
        }
    ).encode("utf-8")
    request = urllib.request.Request(
        f"http://{HOST}:{PORT}/api/v1/analyze",
        data=body,
        headers={
            "Content-Type": "application/json",
            "X-Request-ID": "g3-02-restart",
        },
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=60) as response:
        return json.loads(response.read().decode("utf-8"))


def _start() -> subprocess.Popen:
    env = os.environ.copy()
    env["PYTHONPATH"] = str(ROOT) + os.pathsep + env.get("PYTHONPATH", "")
    return subprocess.Popen(
        [
            sys.executable,
            "-m",
            "uvicorn",
            "applications.api.app:app",
            "--host",
            HOST,
            "--port",
            str(PORT),
        ],
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )


def _stop(proc: subprocess.Popen) -> None:
    if proc.poll() is not None:
        return
    if os.name == "nt":
        proc.terminate()
    else:
        proc.send_signal(signal.SIGTERM)
    try:
        proc.wait(timeout=15)
    except subprocess.TimeoutExpired:
        proc.kill()
        proc.wait(timeout=5)


def main() -> int:
    first = _start()
    try:
        health1 = _wait_health()
        a1 = _analyze()
        dung1 = a1.get("data", {}).get("useful_god", {}).get("useful_display")
    finally:
        _stop(first)
    time.sleep(1)
    second = _start()
    try:
        health2 = _wait_health()
        a2 = _analyze()
        dung2 = a2.get("data", {}).get("useful_god", {}).get("useful_display")
    finally:
        _stop(second)
    expected = "Thủy · Nhâm · Thực Thần"
    payload = {
        "health_1": health1,
        "health_2": health2,
        "dung_1": dung1,
        "dung_2": dung2,
        "ids": [a1.get("request_id"), a2.get("request_id")],
        "pass": health1.get("status") == "ok"
        and health2.get("status") == "ok"
        and dung1 == expected
        and dung2 == expected,
    }
    out = Path(__file__).resolve().parent / "G3_02_RESTART.json"
    out.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"pass": payload["pass"], "dung_match": dung1 == dung2 == expected}, ensure_ascii=True))
    return 0 if payload["pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
