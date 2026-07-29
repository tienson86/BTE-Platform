"""BTE Web Admin package (UI only)."""

from __future__ import annotations

import importlib
from typing import Any

__all__ = ["app", "create_app"]


def __getattr__(name: str) -> Any:
    """Lazy export without shadowing the ``app`` submodule."""
    if name in {"app", "create_app"}:
        mod = importlib.import_module("applications.web_admin.app")
        return getattr(mod, name)
    raise AttributeError(f"module 'applications.web_admin' has no attribute {name!r}")
