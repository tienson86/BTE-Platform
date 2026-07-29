"""Template renderer — HTML files only, no business logic."""

from __future__ import annotations

from pathlib import Path

from applications.web_admin.config import WEB_ADMIN_ROOT
from applications.web_admin.nav import NAV_ITEMS

TEMPLATES_DIR = WEB_ADMIN_ROOT / "templates"


def render_page(template_name: str, *, active: str) -> str:
    """
    Load an HTML template and inject the shared chrome.

    Templates may include ``{{NAV}}`` and ``{{ACTIVE_<key>}}`` placeholders.
    """
    base = (TEMPLATES_DIR / "_layout.html").read_text(encoding="utf-8")
    body = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
    nav_html = []
    for item in NAV_ITEMS:
        cls = "nav-link active" if item.key == active else "nav-link"
        nav_html.append(
            f'<a class="{cls}" href="{item.path}">{item.label}</a>'
        )
    html = base.replace("{{NAV}}", "\n".join(nav_html))
    html = html.replace("{{CONTENT}}", body)
    html = html.replace("{{ACTIVE}}", active)
    for item in NAV_ITEMS:
        html = html.replace(
            f"{{{{ACTIVE_{item.key.upper()}}}}}",
            "active" if item.key == active else "",
        )
    return html
