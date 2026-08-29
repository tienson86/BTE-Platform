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

DATE_SELECTION_NAV: tuple[NavItem, ...] = (
    NavItem("good-date", "nav.good_date", "/good-date", "good_date.html"),
    NavItem("choose-date", "nav.choose_date", "/choose-date", "choose_date.html"),
)
DATE_SELECTION_MENU_LABEL = "nav.date_selection"

# Customer Portal V1 primary product navigation (Commercial Dashboard 00_NAVIGATION).
# Routes stay registered in NAV_ITEMS; only these three appear in the header.
CUSTOMER_NAV_ITEMS: tuple[NavItem, ...] = (
    NavItem("home", "nav.dashboard", "/good-date", "good_date.html"),
    NavItem("choose-date", "nav.choose_date", "/choose-date", "choose_date.html"),
    NavItem("analyze", "nav.view_chart", "/analyze", "analyze.html"),
)

HOME_PATH = "/good-date"

