"""Run the isolated TV-01 customer composition host."""

from __future__ import annotations

import os

import uvicorn

from consulting.marriage.ui.host import create_marriage_customer_app


def main() -> None:
    """Start the isolated Marriage API + customer page."""
    host = os.getenv("BTE_MARRIAGE_HOST", "127.0.0.1")
    port = int(os.getenv("BTE_MARRIAGE_PORT", "8082"))
    uvicorn.run(create_marriage_customer_app(), host=host, port=port)


if __name__ == "__main__":
    main()
