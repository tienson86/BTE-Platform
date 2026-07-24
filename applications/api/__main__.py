"""python -m applications.api"""

from __future__ import annotations

import uvicorn


def main() -> None:
    """Start uvicorn for Applications API."""
    uvicorn.run(
        "applications.api.app:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
