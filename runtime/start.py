"""Start BTE Platform desktop runtime.

Usage:
    python runtime/start.py
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from runtime.manager import start_all  # noqa: E402


def main() -> int:
    """CLI entry for starting all BTE services."""
    return start_all(open_browser=True)


if __name__ == "__main__":
    raise SystemExit(main())
