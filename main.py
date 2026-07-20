"""
BTE Platform

Main Entry Point

File: main.py
Version: 1.0
"""

from __future__ import annotations

import uvicorn


def main() -> None:
    """
    Khởi động BTE Platform.
    """

    uvicorn.run(
        "api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    )


if __name__ == "__main__":
    main()
