"""Applications API package."""

from __future__ import annotations

from typing import Any

__all__ = ["app", "create_app"]


def __getattr__(name: str) -> Any:
    """Lazy-export app factory to avoid import cycles with admin/ops."""
    if name in {"app", "create_app"}:
        from applications.api.app import app as _app
        from applications.api.app import create_app as _create_app

        return _app if name == "app" else _create_app
    raise AttributeError(f"module 'applications.api' has no attribute {name!r}")
