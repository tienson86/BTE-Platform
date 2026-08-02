"""Start BTE Platform desktop runtime.

Usage:
    python runtime/start.py
"""

from __future__ import annotations

import os
import sys
import traceback
from importlib import import_module
from importlib import util as importlib_util
from pathlib import Path


def _step(msg: str) -> None:
    """Print a numbered startup step (ASCII-only for Windows consoles)."""
    print(msg, flush=True)


def _force_utf8_stdio() -> None:
    """Avoid UnicodeEncodeError on Windows cp1252 consoles."""
    os.environ.setdefault("PYTHONIOENCODING", "utf-8")
    for stream_name in ("stdout", "stderr"):
        stream = getattr(sys, stream_name, None)
        if stream is not None and hasattr(stream, "reconfigure"):
            try:
                stream.reconfigure(encoding="utf-8", errors="replace")
            except Exception:
                pass


def _bootstrap_sys_path() -> Path:
    """Put repo root on sys.path; remove script-dir shadowing."""
    script_dir = Path(__file__).resolve().parent
    root = script_dir.parent
    root_s = str(root)
    script_s = str(script_dir)

    def key(entry: str) -> str:
        if not entry:
            return entry
        try:
            return str(Path(entry).resolve())
        except OSError:
            return entry

    skip = {root_s, script_s, str(root.resolve()), str(script_dir.resolve())}
    sys.path[:] = [p for p in sys.path if key(p) not in skip]
    sys.path.insert(0, root_s)
    return root


def _log_import_context(label: str) -> None:
    """Log interpreter context immediately before a critical import."""
    _step(f"  [{label}] sys.executable = {sys.executable}")
    _step(f"  [{label}] cwd = {os.getcwd()}")
    _step(f"  [{label}] sys.path ({len(sys.path)} entries):")
    for index, entry in enumerate(sys.path):
        _step(f"    [{index}] {entry!r}")
    for name in ("dateutil", "pandas"):
        try:
            spec = importlib_util.find_spec(name)
            _step(
                f"  [{label}] find_spec({name!r}) = "
                f"origin={getattr(spec, 'origin', None)!r}"
            )
        except Exception as exc:
            _step(f"  [{label}] find_spec({name!r}) FAILED: {exc}")


def _probe_critical_imports() -> None:
    """
    Import dateutil/pandas before Dependency Resolver.

    On failure: print FULL traceback and exit 1.
    """
    for name in ("dateutil", "pandas"):
        _step(f"STEP 4: probe import {name}")
        _log_import_context(f"before import {name}")
        try:
            mod = import_module(name)
            _step(
                f"STEP 4 OK: import {name} file={getattr(mod, '__file__', None)}"
            )
        except Exception:
            _step(f"STEP 4 FAIL: import {name}")
            traceback.print_exc()
            raise SystemExit(1) from None


_force_utf8_stdio()
_step("STEP 1: force UTF-8 stdio")
_step("STEP 2: bootstrap sys.path")
_ROOT = _bootstrap_sys_path()
_step(f"STEP 2 OK: repo root = {_ROOT}")

_step("STEP 3: import runtime.manager")
from runtime.manager import start_all  # noqa: E402

_step("STEP 3 OK: runtime.manager imported")


def main() -> int:
    """CLI entry for starting all BTE services."""
    _step("STEP 4: critical imports (dateutil, pandas)")
    _probe_critical_imports()
    _step("STEP 5: call start_all(open_browser=True)")
    code = start_all(open_browser=True)
    _step(f"STEP FINAL: start_all returned exit={code}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())
