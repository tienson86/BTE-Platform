"""HTML template renderer."""

from __future__ import annotations

from applications.customer_portal.config import PORTAL_ROOT, settings
from applications.customer_portal.i18n import DEFAULT_LOCALE, dump_catalog_json, load_catalog, t
from applications.customer_portal.pages import LOGIN_ITEM, NAV_ITEMS

TEMPLATES_DIR = PORTAL_ROOT / "templates"


def render_page(template_name: str, *, active: str, locale: str = DEFAULT_LOCALE) -> str:
    """Compose layout + page body with navigation (labels from i18n catalog)."""
    catalog = load_catalog(locale)
    base = (TEMPLATES_DIR / "_layout.html").read_text(encoding="utf-8")
    body = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
    nav_html: list[str] = []
    for item in NAV_ITEMS:
        cls = "nav-link active" if item.key == active else "nav-link"
        label = t(catalog, item.label)
        nav_html.append(f'<a class="{cls}" href="{item.path}">{label}</a>')
    login_label = t(catalog, LOGIN_ITEM.label)
    if active == "login":
        nav_html.insert(
            0,
            f'<a class="nav-link active" href="{LOGIN_ITEM.path}">{login_label}</a>',
        )
    else:
        nav_html.append(
            f'<a class="nav-link" href="{LOGIN_ITEM.path}">{login_label}</a>'
        )
    html = base.replace("{{NAV}}", "\n".join(nav_html))
    html = html.replace("{{CONTENT}}", body)
    html = html.replace("{{ACTIVE}}", active)
    html = html.replace("{{LANG}}", locale)
    html = html.replace("{{I18N_JSON}}", dump_catalog_json(locale))
    html = html.replace("{{I18N_LOCALE}}", locale)
    html = html.replace("{{DOC_TITLE}}", t(catalog, "brand.title") or settings.title)
    return html
