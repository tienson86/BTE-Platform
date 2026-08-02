"""Start BTE Platform desktop runtime.

Usage:
    python runtime/start.py
"""

from __future__ import annotations

import sys
from pathlib import Path

# Must run before ``import runtime`` when invoked as ``python runtime/start.py``.
_ROOT = Path(__file__).resolve().parents[1]
_ROOT_S = str(_ROOT)
sys.path[:] = [p for p in sys.path if p != _ROOT_S]
sys.path.insert(0, _ROOT_S)

from runtime.manager import start_all  # noqa: E402


def main() -> int:
    """CLI entry for starting all BTE services."""
    return start_all(open_browser=True)


if __name__ == "__main__":
    raise SystemExit(main())
