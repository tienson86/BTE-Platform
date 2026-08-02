"""Show BTE Platform service status.

Usage:
    python runtime/status.py
"""

from __future__ import annotations

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
_ROOT_S = str(_ROOT)
sys.path[:] = [p for p in sys.path if p != _ROOT_S]
sys.path.insert(0, _ROOT_S)

from runtime.manager import status_all  # noqa: E402


def main() -> int:
    """CLI entry for service status (Running / Down)."""
    return status_all()


if __name__ == "__main__":
    raise SystemExit(main())
