"""Stop BTE Platform desktop runtime.

Usage:
    python runtime/stop.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_SCRIPT_DIR = Path(__file__).resolve().parent
_ROOT = _SCRIPT_DIR.parent
_SCRIPT_S = str(_SCRIPT_DIR)
_ROOT_S = str(_ROOT)


def _path_key(entry: str) -> str:
    if not entry:
        return entry
    try:
        return str(Path(entry).resolve())
    except OSError:
        return entry


_SKIP = {_ROOT_S, _SCRIPT_S, str(_ROOT.resolve()), str(_SCRIPT_DIR.resolve())}
sys.path[:] = [p for p in sys.path if _path_key(p) not in _SKIP]
sys.path.insert(0, _ROOT_S)

from runtime.manager import stop_all  # noqa: E402


def main() -> int:
    """CLI entry for stopping all BTE services."""
    return stop_all()


if __name__ == "__main__":
    raise SystemExit(main())
