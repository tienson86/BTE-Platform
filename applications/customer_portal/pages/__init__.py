"""Portal page registry."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NavItem:
    """Top/side navigation item (label is an i18n key)."""

    key: str
    label: str
    path: str
    template: str


NAV_ITEMS: tuple[NavItem, ...] = (
    NavItem("dashboard", "nav.dashboard", "/dashboard", "dashboard.html"),
    NavItem("analyze", "nav.analyze", "/analyze", "analyze.html"),
    NavItem("result", "nav.result", "/result", "result.html"),
    NavItem("reports", "nav.reports", "/reports", "reports.html"),
    NavItem("history", "nav.history", "/history", "history.html"),
    NavItem("profile", "nav.profile", "/profile", "profile.html"),
)

LOGIN_ITEM = NavItem("login", "nav.login", "/login", "login.html")
