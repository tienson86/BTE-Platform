"""Portal page registry."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NavItem:
    """Top/side navigation item."""

    key: str
    label: str
    path: str
    template: str


NAV_ITEMS: tuple[NavItem, ...] = (
    NavItem("analyze", "Analyze", "/analyze", "analyze.html"),
    NavItem("result", "Result", "/result", "result.html"),
    NavItem("reports", "Reports", "/reports", "reports.html"),
    NavItem("history", "History", "/history", "history.html"),
    NavItem("profile", "Profile", "/profile", "profile.html"),
)

LOGIN_ITEM = NavItem("login", "Login", "/login", "login.html")
