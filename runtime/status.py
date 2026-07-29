"""Show BTE Platform service status.

Usage:
    python runtime/status.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.manager import status_all  # noqa: E402


def main() -> int:
    """CLI entry for service status (Running / Down)."""
    return status_all()


if __name__ == "__main__":
    raise SystemExit(main())
