"""P0: trace Analyze submit pipeline with DevTools-equivalent probes."""

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

PROBE = """
(() => {
  window.__P0 = { stages: [] };
  function log(stage, extra) {
    const row = Object.assign({ stage: stage, t: Date.now() }, extra || {});
    window.__P0.stages.push(row);
    console.info("[P0-STAGE] " + JSON.stringify(row));
  }
  const origFetch = window.fetch.bind(window);
  window.fetch = function (input, init) {
    const url = typeof input === "string" ? input : (input && input.url) || "";
    const method = (init && init.method) || (input && input.method) || "GET";
    log("fetch_call", { url: String(url), method: String(method) });
    return origFetch(input, init).then(function (res) {
      return res.clone().text().then(function (text) {
        log("fetch_response", {
          url: res.url,
          status: res.status,
          ok: res.ok,
          body_head: String(text || "").slice(0, 500)
        });
        return res;
      });
    }).catch(function (err) {
      log("fetch_reject", { url: String(url), error: String((err && err.stack) || err) });
      throw err;
    });
  };
  const origAssign = window.location.assign.bind(window.location);
  window.location.assign = function (url) {
    log("location_assign", { url: String(url) });
    return origAssign(url);
  };
  function wrapStore() {
    if (!window.BtePortal || !BtePortal.ResultStore || BtePortal.ResultStore.__p0) return false;
    const origSave = BtePortal.saveLastResult.bind(BtePortal);
    BtePortal.saveLastResult = function (payload) {
      const ok = origSave(payload);
      log("resultstore_save", { ok: Boolean(ok), hasData: Boolean(payload && payload.data) });
      return ok;
    };
    const origLoad = BtePortal.ResultStore.load.bind(BtePortal.ResultStore);
    BtePortal.ResultStore.load = function () {
      const value = origLoad();
      log("resultstore_load", { ok: Boolean(value && value.data) });
      return value;
    };
    BtePortal.ResultStore.__p0 = true;
    return true;
  }
  const timer = setInterval(function () {
    if (wrapStore()) clearInterval(timer);
  }, 10);
  document.addEventListener("click", function (ev) {
    const btn = ev.target && ev.target.closest ? ev.target.closest("#btnAnalyze") : null;
    if (!btn) return;
    log("click", {
      id: btn.id,
      type: btn.type,
      disabled: btn.disabled,
      hasOnclick: Boolean(btn.getAttribute("onclick")),
      inForm: Boolean(btn.form),
      formId: btn.form && btn.form.id
    });
  }, true);
  document.addEventListener("submit", function (ev) {
    log("submit_capture", {
      id: ev.target && ev.target.id,
      defaultPrevented: ev.defaultPrevented,
      action: ev.target && ev.target.getAttribute("action")
    });
  }, true);
  document.addEventListener("submit", function (ev) {
    log("submit_bubble", {
      id: ev.target && ev.target.id,
      defaultPrevented: ev.defaultPrevented
    });
  }, false);
})();
"""

INSPECT = """
() => {
  const btn = document.getElementById("btnAnalyze");
  const form = document.getElementById("analyzeForm");
  const date = document.getElementById("birth_date");
  const origSave = window.BtePortal && BtePortal.saveLastResult;
  if (origSave && !origSave.__p0wrapped) {
    BtePortal.saveLastResult = function (payload) {
      const ok = origSave(payload);
      window.__P0.stages.push({
        stage: "resultstore_save",
        t: Date.now(),
        ok: Boolean(ok),
        hasData: Boolean(payload && payload.data)
      });
      return ok;
    };
    BtePortal.saveLastResult.__p0wrapped = true;
  }
  const origLoad = window.BtePortal && BtePortal.ResultStore && BtePortal.ResultStore.load;
  if (origLoad && !origLoad.__p0wrapped) {
    BtePortal.ResultStore.load = function () {
      const value = origLoad();
      window.__P0.stages.push({
        stage: "resultstore_load",
        t: Date.now(),
        ok: Boolean(value && value.data)
      });
      return value;
    };
    BtePortal.ResultStore.load.__p0wrapped = true;
  }
  return {
    btnCount: document.querySelectorAll("#btnAnalyze").length,
    formCount: document.querySelectorAll("#analyzeForm").length,
    dateCount: document.querySelectorAll("#birth_date").length,
    btnType: btn && btn.type,
    btnOnclick: btn && (btn.getAttribute("onclick") || null),
    formAction: form && form.getAttribute("action"),
    formMethod: form && form.getAttribute("method"),
    novalidate: form && form.hasAttribute("novalidate"),
    dateValue: date && date.value,
    datePlaceholder: date && date.placeholder,
    scripts: Array.from(document.scripts).map((s) => s.src || s.textContent.slice(0, 80)),
    hasPortal: Boolean(window.BtePortal),
    hasPost: Boolean(window.BtePortal && window.BtePortal.post),
    hasStore: Boolean(window.BtePortal && window.BtePortal.ResultStore),
    analyzeJsLoaded: Array.from(document.scripts).some((s) => (s.src || "").indexOf("analyze.js") !== -1)
  };
}
"""


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


def _fill_form(page, date_value: str, type_date: bool) -> None:
    page.fill("#full_name", "Nguyen Tien Son")
    page.check("#gender_male")
    page.fill("#birth_date", "")
    if type_date:
        page.locator("#birth_date").press_sequentially(date_value, delay=40)
    else:
        page.fill("#birth_date", date_value)
    page.fill("#birth_time", "04:30")
    page.fill("#birth_place", "Ha Tay, Viet Nam")


def _one_run(page, date_value: str, type_date: bool, label: str) -> dict[str, object]:
    console: list[dict[str, str]] = []
    pageerror: list[str] = []
    net: list[dict[str, object]] = []

    def on_console(msg) -> None:
        console.append({"level": msg.type, "text": msg.text})

    def on_pageerror(err) -> None:
        pageerror.append("".join(err.stack or str(err)))

    def on_request(req) -> None:
        if "/backend/api/v1/analyze" in req.url or req.url.endswith("/analyze"):
            net.append(
                {
                    "kind": "request",
                    "method": req.method,
                    "url": req.url,
                    "post_data": req.post_data,
                }
            )

    def on_response(res) -> None:
        if "/backend/api/v1/analyze" in res.url:
            body_head = ""
            try:
                text = res.text()
                body_head = text[:400]
            except Exception as exc:
                body_head = "read_error:" + str(exc)
            net.append(
                {
                    "kind": "response",
                    "status": res.status,
                    "url": res.url,
                    "body_head": body_head,
                }
            )

    def on_fail(req) -> None:
        net.append({"kind": "requestfailed", "url": req.url, "error": str(req.failure)})

    page.on("console", on_console)
    page.on("pageerror", on_pageerror)
    page.on("request", on_request)
    page.on("response", on_response)
    page.on("requestfailed", on_fail)

    page.goto(f"{BASE}/analyze", wait_until="networkidle")
    inspect = page.evaluate(INSPECT)
    _fill_form(page, date_value, type_date)
    after_fill = page.evaluate(
        """() => ({
          date: document.getElementById('birth_date').value,
          time: document.getElementById('birth_time').value,
          name: document.getElementById('full_name').value,
          place: document.getElementById('birth_place').value,
          gender: document.querySelector('input[name=gender]:checked') && document.querySelector('input[name=gender]:checked').value
        })"""
    )
    page.click("#btnAnalyze")
    redirected = False
    redirect_url = ""
    try:
        page.wait_for_url("**/result", timeout=60000)
        redirected = True
        redirect_url = page.url
    except Exception as exc:
        redirect_url = page.url + " | " + str(exc)

    probe = None
    flash = ""
    date_err = ""
    status = ""
    try:
        flash = page.locator("#globalFlash").inner_text()
        date_err = page.locator("#err_birth_date").inner_text()
        status = page.locator("#analyzeStatus").inner_text()
    except Exception:
        pass

    stages = []
    for row in console:
        text = row.get("text") or ""
        if text.startswith("[P0-STAGE] "):
            try:
                stages.append(json.loads(text[len("[P0-STAGE] "):]))
            except Exception:
                stages.append({"raw": text})

    return {
        "label": label,
        "date_value": date_value,
        "typed": type_date,
        "inspect": inspect,
        "after_fill": after_fill,
        "redirected": redirected,
        "redirect_url": redirect_url,
        "flash": flash,
        "date_err": date_err,
        "status": status,
        "stages": stages,
        "console": console,
        "pageerror": pageerror,
        "network": net,
    }


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    repeats = int(os.environ.get("P0_REPEATS", "1"))
    date_value = os.environ.get("P0_DATE", "21/01/1987")
    type_date = os.environ.get("P0_TYPE", "1") == "1"
    tag = os.environ.get("P0_TAG", "trace")
    _kill_port(API_PORT)
    _kill_port(PORTAL_PORT)
    api_proc = _spawn("applications.api.app:app", API_PORT)
    portal_proc = _spawn("applications.customer_portal.app:app", PORTAL_PORT)
    runs: list[dict[str, object]] = []
    try:
        _wait(API_PORT)
        _wait(PORTAL_PORT)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch()
            for index in range(repeats):
                page = browser.new_page(viewport={"width": 1280, "height": 900}, locale="en-US")
                page.add_init_script(PROBE)
                runs.append(_one_run(page, date_value, type_date, f"{tag}_{index + 1}"))
                page.screenshot(path=str(OUT / f"{tag}_{index + 1}.png"), full_page=True)
                page.close()
            browser.close()
    finally:
        out_json = OUT / f"{tag}.json"
        out_json.write_text(json.dumps(runs, ensure_ascii=True, indent=2), encoding="utf-8")
        print("wrote", out_json)
        for proc in (portal_proc, api_proc):
            proc.terminate()
            try:
                proc.wait(timeout=5)
            except subprocess.TimeoutExpired:
                proc.kill()


if __name__ == "__main__":
    main()
