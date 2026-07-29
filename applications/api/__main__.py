"""python -m applications.api"""

from __future__ import annotations

import uvicorn


def main() -> None:
    """Start Applications API with uvicorn."""
    uvicorn.run(
        "applications.api.app:app",
        host="127.0.0.1",
        port=8000,
        reload=False,
    )


if __name__ == "__main__":
    main()
