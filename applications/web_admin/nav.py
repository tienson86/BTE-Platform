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
    NavItem("dashboard", "Tổng quan", "/", "dashboard.html"),
    NavItem("accounts", "Quản lý tài khoản", "/accounts", "accounts.html"),
    NavItem("memberships", "Thành viên & thanh toán", "/memberships", "membership.html"),
    NavItem("website-settings", "Cấu hình website", "/website-settings", "membership.html"),
    NavItem("customers", "Khách hàng", "/customers", "customers.html"),
    NavItem("cases", "Hồ sơ tư vấn", "/cases", "cases.html"),
    NavItem("reports", "Báo cáo", "/reports", "reports.html"),
    NavItem("licenses", "Bản quyền", "/licenses", "licenses.html"),
    NavItem("statistics", "Thống kê", "/statistics", "statistics.html"),
    NavItem("settings", "Thông tin hệ thống", "/settings", "settings.html"),
)
