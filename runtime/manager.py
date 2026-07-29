"""Service manager for API, Web Admin, and Customer Portal (runtime only)."""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from importlib import import_module
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
RUNTIME_DIR = Path(__file__).resolve().parent
LOG_DIR = RUNTIME_DIR / "logs"
RUN_DIR = RUNTIME_DIR / "run"
SERVICES_CONFIG = ROOT / "configs" / "services.json"
VERSION_FILE = ROOT / "VERSION"
PORTAL_URL = "http://localhost:8081"

REQUIRED_IMPORTS: tuple[str, ...] = (
    "fastapi",
    "uvicorn",
    "pydantic",
    "httpx",
    "pandas",
    "numpy",
    "yaml",
    "openpyxl",
    "dateutil",
)

HEALTH_TIMEOUT_SEC = 45.0
HEALTH_POLL_SEC = 0.5


@dataclass(slots=True)
class ServiceSpec:
    """One runnable UI/API process."""

    key: str
    label: str
    module: str
    host: str
    port: int
    health_path: str
    log_name: str

    @property
    def base_url(self) -> str:
        """HTTP base URL for this service."""
        return f"http://{self.host}:{self.port}"

    @property
    def health_url(self) -> str:
        """Full health check URL."""
        return f"{self.base_url}{self.health_path}"

    @property
    def pid_path(self) -> Path:
        """Path to PID file."""
        return RUN_DIR / f"{self.key}.pid"

    @property
    def log_path(self) -> Path:
        """Path to service log file under runtime/logs."""
        return LOG_DIR / self.log_name


@dataclass(slots=True)
class HealthResult:
    """Result of a single health probe."""

    running: bool
    reason: str
    status_code: int | None = None


@dataclass(slots=True)
class CheckResult:
    """Preflight check outcome."""

    ok: bool
    message: str


def read_version() -> str:
    """Return platform version from VERSION file."""
    if VERSION_FILE.is_file():
        text = VERSION_FILE.read_text(encoding="utf-8").strip()
        if text:
            return text
    return "1.0.0"


def ensure_dirs() -> None:
    """Create runtime log/run directories and common data folders."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    RUN_DIR.mkdir(parents=True, exist_ok=True)
    (ROOT / "logs").mkdir(parents=True, exist_ok=True)
    (ROOT / "reports").mkdir(parents=True, exist_ok=True)
    (ROOT / "applications" / "data").mkdir(parents=True, exist_ok=True)


def load_services() -> list[ServiceSpec]:
    """Load service definitions from configs/services.json."""
    raw = json.loads(SERVICES_CONFIG.read_text(encoding="utf-8"))
    services = raw.get("services") or {}
    host = "127.0.0.1"
    order = ("api", "web_admin", "customer_portal")
    labels = {
        "api": "API",
        "web_admin": "Admin",
        "customer_portal": "Portal",
    }
    result: list[ServiceSpec] = []
    for key in order:
        entry = services[key]
        result.append(
            ServiceSpec(
                key=key,
                label=labels[key],
                module=str(entry["module"]),
                host=host,
                port=int(entry["port"]),
                health_path=str(entry["health"]),
                log_name=f"{key}.log",
            )
        )
    return result


def load_environment() -> dict[str, str]:
    """Build process environment from configs/services.json + current env."""
    env = os.environ.copy()
    env["PYTHONPATH"] = (
        str(ROOT)
        if not env.get("PYTHONPATH")
        else os.pathsep.join([str(ROOT), env["PYTHONPATH"]])
    )
    if SERVICES_CONFIG.is_file():
        raw = json.loads(SERVICES_CONFIG.read_text(encoding="utf-8"))
        for key, value in (raw.get("environment") or {}).items():
            env.setdefault(str(key), str(value))
    env.setdefault("BTE_API_BASE_URL", "http://127.0.0.1:8000")
    env.setdefault("HOST", "127.0.0.1")
    return env


def check_python() -> CheckResult:
    """Verify supported Python version."""
    major, minor = sys.version_info[:2]
    if (major, minor) < (3, 10):
        return CheckResult(
            False,
            f"Python {major}.{minor} is unsupported; require Python >= 3.10 "
            f"(found {sys.executable})",
        )
    return CheckResult(
        True,
        f"Python {major}.{minor}.{sys.version_info[2]} ({sys.executable})",
    )


def check_requirements() -> CheckResult:
    """Verify required third-party packages are importable."""
    missing: list[str] = []
    for name in REQUIRED_IMPORTS:
        try:
            import_module(name)
        except Exception:
            missing.append(name)
    if missing:
        return CheckResult(
            False,
            "Missing packages: "
            + ", ".join(missing)
            + ". Install with: pip install -r requirements.txt "
            "-r applications/requirements.txt",
        )
    return CheckResult(True, f"Required packages OK ({len(REQUIRED_IMPORTS)})")


def check_configuration() -> CheckResult:
    """Verify VERSION, services.json, and application modules."""
    if not VERSION_FILE.is_file():
        return CheckResult(False, f"Missing VERSION file: {VERSION_FILE}")
    if not SERVICES_CONFIG.is_file():
        return CheckResult(False, f"Missing config: {SERVICES_CONFIG}")
    try:
        services = load_services()
    except Exception as exc:
        return CheckResult(False, f"Invalid services.json: {exc}")
    if not services:
        return CheckResult(False, "No services defined in services.json")
    for spec in services:
        module_name = spec.module.split(":", 1)[0]
        try:
            import_module(module_name)
        except Exception as exc:
            return CheckResult(
                False,
                f"Cannot import {module_name}: {exc}",
            )
    return CheckResult(
        True,
        f"Config OK — {len(services)} services, version {read_version()}",
    )


def _read_pid(spec: ServiceSpec) -> int | None:
    if not spec.pid_path.is_file():
        return None
    try:
        text = spec.pid_path.read_text(encoding="utf-8").strip()
        return int(text) if text else None
    except (OSError, ValueError):
        return None


def _write_pid(spec: ServiceSpec, pid: int) -> None:
    spec.pid_path.write_text(str(pid), encoding="utf-8")


def _clear_pid(spec: ServiceSpec) -> None:
    if spec.pid_path.is_file():
        try:
            spec.pid_path.unlink()
        except OSError:
            pass


def _pid_alive(pid: int) -> bool:
    if pid <= 0:
        return False
    if sys.platform == "win32":
        completed = subprocess.run(
            ["tasklist", "/FI", f"PID eq {pid}", "/NH"],
            check=False,
            capture_output=True,
            text=True,
        )
        out = (completed.stdout or "").strip()
        if not out or "No tasks" in out or out.upper().startswith("INFO:"):
            return False
        return str(pid) in out
    try:
        os.kill(pid, 0)
    except ProcessLookupError:
        return False
    except PermissionError:
        return True
    except OSError:
        return False
    return True


def _find_listener_pid(port: int) -> int | None:
    """Best-effort PID for a TCP LISTENING socket on ``port``."""
    if sys.platform == "win32":
        completed = subprocess.run(
            ["netstat", "-ano", "-p", "tcp"],
            check=False,
            capture_output=True,
            text=True,
        )
        needle = f":{port}"
        for line in completed.stdout.splitlines():
            if "LISTENING" not in line.upper():
                continue
            if needle not in line:
                continue
            parts = line.split()
            if len(parts) < 5:
                continue
            # Prefer exact local bind *:port or 127.0.0.1:port
            local = parts[1] if len(parts) > 1 else ""
            if not local.endswith(needle):
                continue
            try:
                pid = int(parts[-1])
            except ValueError:
                continue
            if pid > 0:
                return pid
        return None

    for cmd in (
        ["ss", "-ltnp", f"sport = :{port}"],
        ["lsof", "-nP", f"-iTCP:{port}", "-sTCP:LISTEN"],
    ):
        completed = subprocess.run(cmd, check=False, capture_output=True, text=True)
        if completed.returncode != 0:
            continue
        text = completed.stdout
        if "pid=" in text:
            try:
                return int(text.split("pid=", 1)[1].split(",", 1)[0])
            except (IndexError, ValueError):
                pass
        for token in text.replace(",", " ").split():
            if token.isdigit() and int(token) > 0:
                return int(token)
    return None


def _resolve_pid(spec: ServiceSpec) -> int | None:
    """PID from file, or listener on the service port."""
    pid = _read_pid(spec)
    if pid is not None and _pid_alive(pid):
        return pid
    listener = _find_listener_pid(spec.port)
    if listener is not None:
        _write_pid(spec, listener)
        return listener
    return pid if pid is not None else None


def _tail_log(spec: ServiceSpec, max_lines: int = 12) -> str:
    if not spec.log_path.is_file():
        return "(no log file)"
    try:
        lines = spec.log_path.read_text(encoding="utf-8", errors="replace").splitlines()
    except OSError as exc:
        return f"(cannot read log: {exc})"
    if not lines:
        return "(empty log)"
    return "\n".join(lines[-max_lines:])


def probe_health(spec: ServiceSpec, timeout: float = 1.0) -> HealthResult:
    """HTTP health probe with process/log fallback reason."""
    pid = _read_pid(spec)
    try:
        request = urllib.request.Request(spec.health_url, method="GET")
        with urllib.request.urlopen(request, timeout=timeout) as response:
            code = int(getattr(response, "status", 200) or 200)
            if 200 <= code < 300:
                return HealthResult(True, "healthy", code)
            return HealthResult(
                False,
                f"health returned HTTP {code}",
                code,
            )
    except urllib.error.HTTPError as exc:
        return HealthResult(False, f"health HTTP {exc.code}", int(exc.code))
    except urllib.error.URLError as exc:
        reason = f"not reachable ({exc.reason})"
    except TimeoutError:
        reason = "not reachable (timeout)"
    except Exception as exc:
        reason = f"health error: {exc}"

    if pid is None:
        listener = _find_listener_pid(spec.port)
        if listener is None:
            return HealthResult(False, reason)
        pid = listener
        _write_pid(spec, pid)

    if not _pid_alive(pid):
        return HealthResult(
            False,
            f"{reason}; process PID {pid} is not running\n--- log ---\n{_tail_log(spec)}",
        )
    return HealthResult(
        False,
        f"{reason}; process PID {pid} still alive\n--- log ---\n{_tail_log(spec)}",
    )


def _start_service(spec: ServiceSpec, env: dict[str, str]) -> None:
    ensure_dirs()
    existing = probe_health(spec)
    if existing.running:
        # Adopt an already-running unmanaged process so stop.py can kill it.
        _resolve_pid(spec)
        return

    old_pid = _resolve_pid(spec)
    if old_pid and _pid_alive(old_pid):
        _stop_pid(old_pid)
        _clear_pid(spec)
        time.sleep(0.3)

    log_file = open(spec.log_path, "a", encoding="utf-8")
    log_file.write(
        f"\n===== start {time.strftime('%Y-%m-%d %H:%M:%S')} "
        f"{spec.module} :{spec.port} =====\n"
    )
    log_file.flush()

    cmd = [
        sys.executable,
        "-m",
        "uvicorn",
        spec.module,
        "--host",
        spec.host,
        "--port",
        str(spec.port),
        "--log-level",
        "info",
    ]
    popen_kwargs: dict[str, Any] = {
        "cwd": str(ROOT),
        "env": env,
        "stdout": log_file,
        "stderr": subprocess.STDOUT,
        "stdin": subprocess.DEVNULL,
    }
    if sys.platform == "win32":
        popen_kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
    else:
        popen_kwargs["start_new_session"] = True

    proc = subprocess.Popen(cmd, **popen_kwargs)
    _write_pid(spec, proc.pid)


def _stop_pid(pid: int) -> None:
    if not _pid_alive(pid):
        return
    if sys.platform == "win32":
        subprocess.run(
            ["taskkill", "/PID", str(pid), "/T", "/F"],
            check=False,
            capture_output=True,
            text=True,
        )
        return
    try:
        os.kill(pid, signal.SIGTERM)
    except OSError:
        pass
    deadline = time.time() + 5.0
    while time.time() < deadline and _pid_alive(pid):
        time.sleep(0.2)
    if _pid_alive(pid):
        try:
            os.kill(pid, signal.SIGKILL)
        except OSError:
            pass


def stop_service(spec: ServiceSpec) -> str:
    """Stop one service by PID file or listening port."""
    pid = _resolve_pid(spec)
    if pid is None:
        health = probe_health(spec)
        if health.running:
            return (
                f"{spec.label}: health still OK but PID unknown "
                f"(port {spec.port}) — stop manually"
            )
        return f"{spec.label}: already Down"

    was_alive = _pid_alive(pid)
    _stop_pid(pid)
    # uvicorn may spawn a child that keeps the port; clear listener too.
    leftover = _find_listener_pid(spec.port)
    if leftover is not None:
        _stop_pid(leftover)
        pid = leftover
        was_alive = True
    _clear_pid(spec)

    # Confirm port released.
    time.sleep(0.4)
    still = probe_health(spec)
    if still.running:
        again = _find_listener_pid(spec.port)
        if again is not None:
            _stop_pid(again)
            time.sleep(0.4)
        still = probe_health(spec)
    if still.running:
        return f"{spec.label}: stop attempted (PID {pid}) but health still OK"
    if was_alive:
        return f"{spec.label}: stopped (PID {pid})"
    return f"{spec.label}: cleared stale PID {pid}"


def wait_healthy(spec: ServiceSpec, timeout: float = HEALTH_TIMEOUT_SEC) -> HealthResult:
    """Poll health until success or timeout."""
    deadline = time.time() + timeout
    last = HealthResult(False, "not started")
    while time.time() < deadline:
        last = probe_health(spec)
        if last.running:
            return last
        pid = _read_pid(spec)
        if pid is not None and not _pid_alive(pid):
            return HealthResult(
                False,
                f"process exited early (PID {pid})\n--- log ---\n{_tail_log(spec)}",
            )
        time.sleep(HEALTH_POLL_SEC)
    return HealthResult(
        False,
        f"timeout after {timeout:.0f}s — {last.reason}",
    )


def start_all(*, open_browser: bool = True) -> int:
    """
    Run preflight checks, start all services, verify health, open portal.

    Returns process exit code (0 = success).
    """
    ensure_dirs()
    print("BTE Runtime — preflight")
    print("-" * 40)

    checks = (
        ("Python", check_python),
        ("Requirements", check_requirements),
        ("Configuration", check_configuration),
    )
    for label, fn in checks:
        result = fn()
        mark = "OK" if result.ok else "FAIL"
        print(f"[{mark}] {label}: {result.message}")
        if not result.ok:
            print("\nStartup aborted.")
            return 1

    env = load_environment()
    services = load_services()
    print("-" * 40)
    print("Starting services...")

    for spec in services:
        print(f"  → {spec.label} ({spec.base_url})")
        try:
            _start_service(spec, env)
        except Exception as exc:
            print(f"FAIL starting {spec.label}: {exc}")
            return 1

    print("Waiting for health...")
    failed = False
    for spec in services:
        health = wait_healthy(spec)
        if health.running:
            print(f"  ✓ {spec.label}: Running")
        else:
            failed = True
            print(f"  ✗ {spec.label}: Down")
            print(f"    Reason: {health.reason}")

    if failed:
        print("\nStartup incomplete — see runtime/logs/ for details.")
        return 1

    if open_browser:
        from launcher.open_browser import open_portal

        open_portal(PORTAL_URL)

    version = read_version()
    print()
    print(f"BTE Platform {version}")
    for spec in services:
        print(f"{spec.label:<6} {spec.base_url}")
    print("READY")
    return 0


def stop_all() -> int:
    """Stop all managed services."""
    ensure_dirs()
    print("BTE Runtime — stopping services")
    print("-" * 40)
    try:
        services = load_services()
    except Exception as exc:
        print(f"Cannot load services.json: {exc}")
        return 1
    for spec in services:
        print(stop_service(spec))
    print("Done.")
    return 0


def status_all() -> int:
    """Print Running/Down status for each service."""
    ensure_dirs()
    version = read_version()
    print(f"BTE Platform {version} — status")
    print("-" * 40)
    try:
        services = load_services()
    except Exception as exc:
        print(f"Cannot load services.json: {exc}")
        return 1

    exit_code = 0
    for spec in services:
        health = probe_health(spec)
        state = "Running" if health.running else "Down"
        pid = _resolve_pid(spec) if health.running else _read_pid(spec)
        pid_part = f" PID={pid}" if pid is not None else ""
        print(f"{spec.label:<6} {state:<8} {spec.base_url}{pid_part}")
        if not health.running:
            exit_code = 1
            print(f"       Reason: {health.reason}")
    return exit_code
