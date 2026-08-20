"""Customer presentation for Useful God Hỷ and Dụng reason — does not mutate engine truth."""

from __future__ import annotations

from collections.abc import Mapping, Sequence
from dataclasses import dataclass
from typing import Any

from .reasoning import ARCHETYPE_SINH_TRO, archetype_for_rule, build_customer_reason
from .roles import format_god_roles, resolve_god_token

EMPTY_CUSTOMER_FAVORABLE_DISPLAY = "Chưa có Hỷ thần bổ trợ riêng"
INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY = "Chưa đủ căn cứ xác định Hỷ thần bổ trợ riêng"
KY_SCOPE_NOTE = "Kỵ thần theo quy tắc cân bằng hiện tại"

HY_ROLE_SUPPORTED_INDEPENDENT = "SUPPORTED_INDEPENDENT_ROLE"
HY_ROLE_STATIC_SAME_ELEMENT = "STATIC_SAME_ELEMENT_SIBLING"
HY_ROLE_STATIC_OTHER = "STATIC_OTHER"
HY_ROLE_UNKNOWN = "UNKNOWN"
HY_ROLE_SUPPORTED = HY_ROLE_SUPPORTED_INDEPENDENT
HY_ROLE_STATIC = HY_ROLE_STATIC_OTHER

Role = Mapping[str, str]

_SIBLING_GROUPS: tuple[frozenset[str], ...] = (
    frozenset({"Thực Thần", "Thương Quan"}),
    frozenset({"Chính Quan", "Thất Sát"}),
    frozenset({"Chính Ấn", "Thiên Ấn"}),
    frozenset({"Chính Tài", "Thiên Tài"}),
    frozenset({"Tỷ Kiên", "Kiếp Tài"}),
)

_PEER_SUPPORT = frozenset({"Tỷ Kiên", "Kiếp Tài"})


def role_identity(role: Role | None) -> tuple[str, str, str]:
    """Return ``(element, stem, ten_god)`` for exact-duplicate comparison."""
    if not role:
        return ("", "", "")
    return (
        str(role.get("element") or "").strip(),
        str(role.get("stem") or "").strip(),
        str(role.get("ten_god") or "").strip(),
    )


def is_exact_dung_duplicate(role: Role | None, dung_role: Role | None) -> bool:
    """True only when element, stem, and Ten God all match and are non-empty."""
    left = role_identity(role)
    right = role_identity(dung_role)
    if not all(left) or not all(right):
        return False
    return left == right


def _is_sibling_ten_god(dung_tg: str, hy_tg: str) -> bool:
    pair = frozenset({dung_tg, hy_tg})
    return any(pair <= group for group in _SIBLING_GROUPS)


def classify_hy_role(
    dung_role: Role | None,
    hy_role: Role | None,
    *,
    winning_rule_id: str = "",
) -> str:
    """Classify leftover Hỷ. Sibling grouping is not independent evidence."""
    dung_el, _, dung_tg = role_identity(dung_role)
    hy_el, _, hy_tg = role_identity(hy_role)
    if not dung_tg or not hy_tg:
        return HY_ROLE_UNKNOWN
    archetype = archetype_for_rule(winning_rule_id)
    if archetype == ARCHETYPE_SINH_TRO and hy_tg in _PEER_SUPPORT:
        return HY_ROLE_SUPPORTED_INDEPENDENT
    same_element = bool(dung_el and hy_el and dung_el == hy_el)
    if same_element and _is_sibling_ten_god(dung_tg, hy_tg):
        return HY_ROLE_STATIC_SAME_ELEMENT
    return HY_ROLE_STATIC_OTHER


def customer_favorable_roles(
    dung_role: Role | None,
    favorable_roles: Sequence[Role] | None,
) -> list[dict[str, str]]:
    """Copy favorable roles excluding the exact Overall Dụng triple."""
    out: list[dict[str, str]] = []
    for role in favorable_roles or ():
        if is_exact_dung_duplicate(role, dung_role):
            continue
        out.append(dict(role))
    return out


@dataclass(slots=True)
class CustomerHyPresentation:
    """Customer Hỷ after exact-Dụng omit + independent-role gate."""

    remaining_roles: list[dict[str, str]]
    supported_roles: list[dict[str, str]]
    classifications: list[str]
    display: str
    role_status: str


def build_customer_hy_presentation(
    dung_role: Role | None,
    favorable_roles: Sequence[Role] | None,
    *,
    winning_rule_id: str = "",
) -> CustomerHyPresentation:
    """Apply HK-R1F omit then independent-role gate. Never reinsert Dụng."""
    remaining = customer_favorable_roles(dung_role, favorable_roles)
    if not remaining:
        return CustomerHyPresentation(
            remaining_roles=[],
            supported_roles=[],
            classifications=[],
            display=EMPTY_CUSTOMER_FAVORABLE_DISPLAY,
            role_status=HY_ROLE_UNKNOWN if not favorable_roles else HY_ROLE_STATIC_OTHER,
        )
    labels = [
        classify_hy_role(dung_role, role, winning_rule_id=winning_rule_id)
        for role in remaining
    ]
    supported = [
        role
        for role, status in zip(remaining, labels, strict=True)
        if status == HY_ROLE_SUPPORTED_INDEPENDENT
    ]
    if supported:
        status = HY_ROLE_SUPPORTED_INDEPENDENT
        display = format_god_roles(supported)
    elif HY_ROLE_STATIC_SAME_ELEMENT in labels:
        status = HY_ROLE_STATIC_SAME_ELEMENT
        display = INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
    elif HY_ROLE_STATIC_OTHER in labels:
        status = HY_ROLE_STATIC_OTHER
        display = INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
    else:
        status = HY_ROLE_UNKNOWN
        display = INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
    return CustomerHyPresentation(
        remaining_roles=remaining,
        supported_roles=supported,
        classifications=labels,
        display=display,
        role_status=status,
    )


def customer_favorable_display(
    dung_role: Role | None,
    favorable_roles: Sequence[Role] | None,
    *,
    winning_rule_id: str = "",
) -> str:
    """Format customer Hỷ. Exact Dụng omitted; STATIC leftover is not a confident Hỷ."""
    return build_customer_hy_presentation(
        dung_role, favorable_roles, winning_rule_id=winning_rule_id
    ).display


def customer_favorable_tokens(
    day_master: str,
    useful_token: str | None,
    favorable_tokens: Sequence[str] | None,
    *,
    winning_rule_id: str = "",
) -> list[str]:
    """Drop exact Dụng and STATIC leftovers from CSV tokens."""
    dung = resolve_god_token(day_master, str(useful_token or ""))
    remaining: list[tuple[str, dict[str, str]]] = []
    for token in favorable_tokens or ():
        text = str(token or "").strip()
        if not text:
            continue
        role = resolve_god_token(day_master, text)
        if is_exact_dung_duplicate(role, dung):
            continue
        remaining.append((text, role))
    out: list[str] = []
    for text, role in remaining:
        status = classify_hy_role(dung, role, winning_rule_id=winning_rule_id)
        if status == HY_ROLE_SUPPORTED_INDEPENDENT:
            out.append(text)
    return out


def customer_hy_overlay_text(
    day_master: str,
    useful_token: str | None,
    favorable_tokens: Sequence[str] | None,
    *,
    winning_rule_id: str = "",
) -> str:
    """Pattern overlay Hỷ string from the same customer policy."""
    supported = customer_favorable_tokens(
        day_master,
        useful_token,
        favorable_tokens,
        winning_rule_id=winning_rule_id,
    )
    if supported:
        return ", ".join(supported)
    dung = resolve_god_token(day_master, str(useful_token or ""))
    leftover = False
    had_src = False
    for token in favorable_tokens or ():
        text = str(token or "").strip()
        if not text:
            continue
        had_src = True
        role = resolve_god_token(day_master, text)
        if not is_exact_dung_duplicate(role, dung):
            leftover = True
            break
    if leftover:
        return INSUFFICIENT_CUSTOMER_FAVORABLE_DISPLAY
    if had_src:
        return EMPTY_CUSTOMER_FAVORABLE_DISPLAY
    return ""


def dung_role_from_result(result: Any) -> dict[str, str]:
    """Build the Overall Dụng role from an engine result or view."""
    return {
        "element": str(getattr(result, "useful_element", "") or ""),
        "stem": str(getattr(result, "useful_stem", "") or ""),
        "ten_god": str(getattr(result, "useful_ten_god", "") or ""),
    }


def customer_reason_from_result(result: Any) -> dict[str, str]:
    """Presentation-safe reason dict. Engine ``reasoning`` stays CSV text."""
    return build_customer_reason(result).to_dict()
