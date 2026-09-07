"""Run the isolated TV-01 Public API host."""

from __future__ import annotations

import os

import uvicorn

from consulting.marriage.api.http import create_marriage_api_app


def main() -> None:
    """Start the B06 Public API without customer pages."""
    host = os.getenv("BTE_MARRIAGE_HOST", "127.0.0.1")
    port = int(os.getenv("BTE_MARRIAGE_PORT", "8082"))
    uvicorn.run(create_marriage_api_app(), host=host, port=port)


if __name__ == "__main__":
    main()
