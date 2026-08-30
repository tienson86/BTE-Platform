"""HTML template renderer."""

from __future__ import annotations

from typing import Any

from applications.customer_portal.config import PORTAL_ROOT, settings
from applications.customer_portal.i18n import DEFAULT_LOCALE, dump_catalog_json, load_catalog, t
from applications.customer_portal.pages import CUSTOMER_NAV_ITEMS

TEMPLATES_DIR = PORTAL_ROOT / "templates"

_ANALYZE_ACTIVE = frozenset({"analyze", "result", "interpretation"})
_HOME_ACTIVE = frozenset({"home", "good-date", ""})


def _is_customer_nav_active(item_key: str, active: str) -> bool:
    """Return whether a customer primary-nav item matches the current page."""
    if item_key == "home":
        return active in _HOME_ACTIVE
    if item_key == "choose-date":
        return active == "choose-date"
    if item_key == "analyze":
        return active in _ANALYZE_ACTIVE
    return item_key == active


def _customer_nav_html(catalog: dict[str, Any], active: str) -> str:
    """Render the three canonical customer product links."""
    links: list[str] = []
    for item in CUSTOMER_NAV_ITEMS:
        is_active = _is_customer_nav_active(item.key, active)
        cls = "nav-link active" if is_active else "nav-link"
        current = ' aria-current="page"' if is_active else ""
        links.append(
            f'<a class="{cls}" href="{item.path}" data-nav-id="{item.key}"{current}>'
            f"{t(catalog, item.label)}</a>"
        )
    return "\n".join(links)


def _customer_header_html(
    catalog: dict[str, Any],
    active: str,
    *,
    skip_href: str = "#mainContent",
) -> str:
    """Render the single Customer Portal chrome used by HTML pages and /result."""
    nav = _customer_nav_html(catalog, active)
    return (
        f'<a class="skip-link" href="{skip_href}">Skip to content</a>\n'
        '  <header class="app-header" id="appHeader">\n'
        '      <a class="app-brand" href="/good-date">BTE <span>Portal</span></a>\n'
        '      <button type="button" class="app-nav-toggle" id="btnNavToggle"'
        ' aria-label="Mở điều hướng" aria-controls="appNav" aria-expanded="false">\n'
        '        <span class="app-nav-toggle__bar" aria-hidden="true"></span>\n'
        '        <span class="app-nav-toggle__bar" aria-hidden="true"></span>\n'
        '        <span class="app-nav-toggle__bar" aria-hidden="true"></span>\n'
        "      </button>\n"
        f'      <nav class="app-nav nav" id="appNav" data-customer-nav="primary"'
        f' aria-label="Điều hướng chính">{nav}</nav>\n'
        '      <div class="app-header-actions">\n'
        '        <button type="button" id="btnThemeToggle" class="secondary"'
        ' aria-pressed="false">Dark</button>\n'
        '        <a class="app-user" href="/profile" aria-label="Hồ sơ" title="Hồ sơ">\n'
        '          <span class="app-user__avatar" aria-hidden="true">U</span>\n'
        "        </a>\n"
        "      </div>\n"
        "    </header>"
    )


def _apply_common_tokens(html: str, *, locale: str, catalog: dict[str, Any]) -> str:
    """Replace shared template tokens."""
    html = html.replace("{{LANG}}", locale)
    html = html.replace("{{I18N_JSON}}", dump_catalog_json(locale))
    html = html.replace("{{I18N_LOCALE}}", locale)
    html = html.replace("{{DOC_TITLE}}", t(catalog, "brand.title") or settings.title)
    html = html.replace("{{NARRATIVE_PROVIDER}}", settings.narrative_provider)
    return html


def render_page(template_name: str, *, active: str, locale: str = DEFAULT_LOCALE) -> str:
    """Compose layout + page body with navigation (labels from i18n catalog)."""
    catalog = load_catalog(locale)
    base = (TEMPLATES_DIR / "_layout.html").read_text(encoding="utf-8")
    body = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
    html = base.replace("{{HEADER}}", _customer_header_html(catalog, active))
    html = html.replace("{{CONTENT}}", body)
    html = html.replace("{{ACTIVE}}", active)
    return _apply_common_tokens(html, locale=locale, catalog=catalog)


def render_desktop_page(
    template_name: str = "result_desktop.html",
    *,
    locale: str = DEFAULT_LOCALE,
    active: str = "analyze",
    skip_href: str = "#rp-main",
) -> str:
    """Render Canonical Desktop V2 host with the shared Customer Portal chrome."""
    catalog = load_catalog(locale)
    html = (TEMPLATES_DIR / template_name).read_text(encoding="utf-8")
    if "{{HEADER}}" in html:
        html = html.replace(
            "{{HEADER}}",
            _customer_header_html(catalog, active, skip_href=skip_href),
        )
    return _apply_common_tokens(html, locale=locale, catalog=catalog)
