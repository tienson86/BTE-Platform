"""Open the BTE Customer Portal in the default browser."""

from __future__ import annotations

import webbrowser


DEFAULT_PORTAL_URL = "http://localhost:8081"


def open_portal(url: str = DEFAULT_PORTAL_URL) -> None:
    """Open ``url`` in the system default browser."""
    webbrowser.open(url)


def main() -> int:
    """CLI entry for opening the Customer Portal."""
    open_portal()
    print(f"Opened {DEFAULT_PORTAL_URL}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
