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

# Free tools are always visible; member tools live in the left sidebar.
CUSTOMER_PUBLIC_NAV_ITEMS: tuple[NavItem, ...] = (
    NavItem("home", "nav.dashboard", "/good-date", "good_date.html"),
    NavItem("name-analysis", "nav.name_analysis", "/name-analysis", "name_analysis.html"),
    NavItem(
        "number-energy",
        "nav.number_energy",
        "/number-energy",
        "number_energy.html",
    ),
)
CUSTOMER_MEMBER_NAV_ITEMS: tuple[NavItem, ...] = (
    NavItem("analyze", "nav.view_chart", "/analyze", "analyze.html"),
    NavItem("choose-date", "nav.choose_date", "/choose-date", "choose_date.html"),
    NavItem(
        "marriage-consulting",
        "nav.marriage_consulting",
        "/marriage-consulting",
        "marriage_consulting.html",
    ),
    NavItem(
        "childbirth-consulting",
        "nav.childbirth_consulting",
        "/childbirth-consulting",
        "childbirth_consulting.html",
    ),
    NavItem(
        "naming-consulting",
        "nav.naming_consulting",
        "/naming-consulting",
        "naming_consulting.html",
    ),
    NavItem("business-consulting", "nav.business_consulting", "/business-consulting", "business_consulting.html"),
    NavItem("van-han", "nav.van_han", "/tinh-van-han", "van_han.html"),
)
CUSTOMER_NAV_ITEMS = CUSTOMER_PUBLIC_NAV_ITEMS + CUSTOMER_MEMBER_NAV_ITEMS

HOME_PATH = "/good-date"
MARRIAGE_CONSULTING_PATH = "/marriage-consulting"
BUSINESS_CONSULTING_PATH = "/business-consulting"
CHILDBIRTH_CONSULTING_PATH = "/childbirth-consulting"
NAMING_CONSULTING_PATH = "/naming-consulting"
NAME_ANALYSIS_PATH = "/name-analysis"
MARRIAGE_API_PROXY_PREFIX = "api/v1/consulting/marriage"
CHILDBIRTH_API_PROXY_PREFIX = "api/v1/consulting/childbirth"
NAMING_API_PROXY_PREFIX = "api/v1/consulting/naming"
CURRENT_NAME_API_PROXY_PREFIX = "api/v1/public/naming"
NUMBER_ENERGY_API_PROXY_PREFIX = "api/v1/number-energy"
NUMBER_ENERGY_PATH = "/number-energy"
NUMBER_ENERGY_ITEM = NavItem(
    "number-energy",
    "nav.number_energy",
    NUMBER_ENERGY_PATH,
    "number_energy.html",
)

