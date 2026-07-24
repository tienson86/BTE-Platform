"""Launch BTE Platform (desktop runtime entry).

Usage:
    python launcher/run_bte.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.manager import start_all  # noqa: E402


def main() -> int:
    """Start API, Admin, Portal, then open the Customer Portal browser."""
    return start_all(open_browser=True)


if __name__ == "__main__":
    raise SystemExit(main())
