"""python -m applications.web_admin"""

from __future__ import annotations

import uvicorn

from applications.web_admin.config import settings


def main() -> None:
    """Start Web Admin UI server."""
    uvicorn.run(
        "applications.web_admin.app:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )


if __name__ == "__main__":
    main()
