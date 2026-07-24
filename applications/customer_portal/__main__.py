"""python -m applications.customer_portal"""

from __future__ import annotations

import uvicorn

from applications.customer_portal.config import settings


def main() -> None:
    """Start Customer Portal UI server."""
    uvicorn.run(
        "applications.customer_portal.app:app",
        host=settings.host,
        port=settings.port,
        reload=False,
    )


if __name__ == "__main__":
    main()
