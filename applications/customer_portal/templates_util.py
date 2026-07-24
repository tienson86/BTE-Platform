"""HTML template renderer."""

from __future__ import annotations

from applications.customer_portal.config import PORTAL_ROOT
from applications.customer_portal.pages import LOGIN_ITEM, NAV_ITEMS

TEMPLATES_DIR = PORTAL_ROOT / "templates"


def render_page(template_name: str, *, active: str) -> str:
    """Compose layout + page body with navigation."""
    base = (TEMPLATES_DIR / "_layout.html").read_text(encoding="utf-8")
    body = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
    items = NAV_ITEMS if active != "login" else (LOGIN_ITEM,)
    # Always show main nav except emphasize login on login page
    nav_source = NAV_ITEMS
    nav_html = []
    for item in nav_source:
        cls = "nav-link active" if item.key == active else "nav-link"
        nav_html.append(f'<a class="{cls}" href="{item.path}">{item.label}</a>')
    if active == "login":
        nav_html.insert(
            0,
            f'<a class="nav-link active" href="{LOGIN_ITEM.path}">{LOGIN_ITEM.label}</a>',
        )
    else:
        nav_html.append(
            f'<a class="nav-link" href="{LOGIN_ITEM.path}">{LOGIN_ITEM.label}</a>'
        )
    html = base.replace("{{NAV}}", "\n".join(nav_html))
    html = html.replace("{{CONTENT}}", body)
    html = html.replace("{{ACTIVE}}", active)
    del items  # reserved for future use
    return html
