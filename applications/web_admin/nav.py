"""Navigation and page registry (no business logic)."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class NavItem:
    """Sidebar navigation entry."""

    key: str
    label: str
    path: str
    template: str


NAV_ITEMS: tuple[NavItem, ...] = (
    NavItem("dashboard", "Dashboard", "/", "dashboard.html"),
    NavItem("customers", "Customers", "/customers", "customers.html"),
    NavItem("cases", "Cases", "/cases", "cases.html"),
    NavItem("reports", "Reports", "/reports", "reports.html"),
    NavItem("licenses", "Licenses", "/licenses", "licenses.html"),
    NavItem("statistics", "Statistics", "/statistics", "statistics.html"),
    NavItem("settings", "Settings", "/settings", "settings.html"),
)
