"""HTML template renderer."""

from __future__ import annotations

from applications.customer_portal.config import PORTAL_ROOT, settings
from applications.customer_portal.i18n import DEFAULT_LOCALE, dump_catalog_json, load_catalog, t
from applications.customer_portal.pages import (
    DATE_SELECTION_MENU_LABEL,
    DATE_SELECTION_NAV,
    LOGIN_ITEM,
    NAV_ITEMS,
)

TEMPLATES_DIR = PORTAL_ROOT / "templates"


def _date_selection_nav_html(catalog: dict[str, str], active: str) -> str:
    """Render the Ngày tốt dropdown (exactly two public items)."""
    toggle_cls = "nav-link nav-dropdown__toggle"
    if active in {"good-date", "choose-date"}:
        toggle_cls += " active"
    links: list[str] = []
    for item in DATE_SELECTION_NAV:
        cls = "nav-dropdown__link active" if item.key == active else "nav-dropdown__link"
        links.append(
            f'<a class="{cls}" href="{item.path}" role="menuitem">{t(catalog, item.label)}</a>'
        )
    return (
        '<div class="nav-dropdown">'
        f'<button type="button" class="{toggle_cls}" aria-expanded="false" '
        f'aria-haspopup="menu">{t(catalog, DATE_SELECTION_MENU_LABEL)}</button>'
        f'<div class="nav-dropdown__menu" role="menu">{"".join(links)}</div>'
        "</div>"
    )


def _apply_common_tokens(html: str, *, locale: str, catalog: dict[str, str]) -> str:
    """Replace shared template tokens."""
    html = html.replace("{{LANG}}", locale)
    html = html.replace("{{I18N_JSON}}", dump_catalog_json(locale))
    html = html.replace("{{I18N_LOCALE}}", locale)
    html = html.replace("{{DOC_TITLE}}", t(catalog, "brand.title") or settings.title)
    return html


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
        if item.key == "analyze":
            nav_html.append(_date_selection_nav_html(catalog, active))
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
    return _apply_common_tokens(html, locale=locale, catalog=catalog)


def render_desktop_page(
    template_name: str = "result_desktop.html",
    *,
    locale: str = DEFAULT_LOCALE,
) -> str:
    """Render full-bleed Canonical Desktop V2 host (no legacy app-shell)."""
    catalog = load_catalog(locale)
    html = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
    return _apply_common_tokens(html, locale=locale, catalog=catalog)
