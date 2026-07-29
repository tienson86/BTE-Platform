"""Portal UI localization (presentation text only)."""

from __future__ import annotations

import json
from functools import lru_cache
from typing import Any

from applications.customer_portal.config import PORTAL_ROOT

DEFAULT_LOCALE = "vi"
I18N_DIR = PORTAL_ROOT / "static" / "i18n"


@lru_cache(maxsize=8)
def load_catalog(locale: str = DEFAULT_LOCALE) -> dict[str, Any]:
    """Load a locale JSON catalog (falls back to Vietnamese)."""
    code = (locale or DEFAULT_LOCALE).strip().lower() or DEFAULT_LOCALE
    path = I18N_DIR / f"{code}.json"
    if not path.is_file():
        path = I18N_DIR / f"{DEFAULT_LOCALE}.json"
    return json.loads(path.read_text(encoding="utf-8"))


def t(catalog: dict[str, Any], key: str, **kwargs: Any) -> str:
    """Resolve a dotted key from the catalog with optional ``{var}`` substitution."""
    node: Any = catalog
    for part in key.split("."):
        if not isinstance(node, dict) or part not in node:
            return key
        node = node[part]
    if not isinstance(node, str):
        return key
    text = node
    for name, value in kwargs.items():
        text = text.replace("{" + name + "}", str(value))
    return text


def dump_catalog_json(locale: str = DEFAULT_LOCALE) -> str:
    """Serialize catalog for embedding in HTML (safe for ``<script>``)."""
    return json.dumps(load_catalog(locale), ensure_ascii=False, separators=(",", ":"))
