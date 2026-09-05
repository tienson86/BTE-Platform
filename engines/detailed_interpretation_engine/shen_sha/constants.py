"""Canonical Shen Sha identities, routing, and cluster families.

Star IDs reuse the upstream BaZi catalog. Extra freeze IDs stay dormant
until the detector publishes them.
"""

from __future__ import annotations

from typing import Final, Mapping

ID_TIAN_YI: Final[str] = "tian_yi"
ID_WEN_CHANG: Final[str] = "wen_chang"
ID_LU_SHEN: Final[str] = "lu_shen"
ID_HONG_LUAN: Final[str] = "hong_luan"
ID_TIAN_XI: Final[str] = "tian_xi"
ID_HUA_GAI: Final[str] = "hua_gai"
ID_YANG_REN: Final[str] = "yang_ren"
ID_TIAN_DE: Final[str] = "tian_de"
ID_YUE_DE: Final[str] = "yue_de"
ID_GUO_YIN: Final[str] = "guo_yin"
ID_HOC_DUONG: Final[str] = "hoc_duong"
ID_THAI_CUC: Final[str] = "thai_cuc"
ID_HAM_TRI: Final[str] = "ham_tri"
ID_GIAI_THAN: Final[str] = "giai_than"
ID_KHONG_VONG: Final[str] = "khong_vong"
ID_CO_THAN: Final[str] = "co_than"
ID_QUA_TU: Final[str] = "qua_tu"

UPSTREAM_CATALOG_IDS: Final[tuple[str, ...]] = (
    ID_TIAN_YI,
    ID_WEN_CHANG,
    ID_LU_SHEN,
    ID_HONG_LUAN,
    ID_TIAN_XI,
    ID_HUA_GAI,
    ID_YANG_REN,
    ID_TIAN_DE,
    ID_YUE_DE,
)

DORMANT_IDS: Final[tuple[str, ...]] = (
    ID_GUO_YIN,
    ID_HOC_DUONG,
    ID_THAI_CUC,
    ID_HAM_TRI,
    ID_GIAI_THAN,
    ID_KHONG_VONG,
    ID_CO_THAN,
    ID_QUA_TU,
)

KNOWN_STAR_IDS: Final[frozenset[str]] = frozenset(UPSTREAM_CATALOG_IDS + DORMANT_IDS)

STAR_DISPLAY_NAMES: Final[Mapping[str, str]] = {
    ID_TIAN_YI: "Thiên Ất Quý Nhân",
    ID_WEN_CHANG: "Văn Xương",
    ID_LU_SHEN: "Lộc Thần",
    ID_HONG_LUAN: "Hồng Loan",
    ID_TIAN_XI: "Thiên Hỷ",
    ID_HUA_GAI: "Hoa Cái",
    ID_YANG_REN: "Dương Nhẫn",
    ID_TIAN_DE: "Thiên Đức Quý Nhân",
    ID_YUE_DE: "Nguyệt Đức Quý Nhân",
    ID_GUO_YIN: "Quốc Ấn",
    ID_HOC_DUONG: "Học Đường",
    ID_THAI_CUC: "Thái Cực",
    ID_HAM_TRI: "Hàm Trì",
    ID_GIAI_THAN: "Giải Thần",
    ID_KHONG_VONG: "Không Vong",
    ID_CO_THAN: "Cô Thần",
    ID_QUA_TU: "Quả Tú",
}

STAR_ALIASES: Final[Mapping[str, tuple[str, ...]]] = {
    ID_TIAN_YI: ("Thiên Ất",),
    ID_TIAN_DE: ("Thiên Đức",),
    ID_YUE_DE: ("Nguyệt Đức",),
}

NAME_TO_ID: Final[dict[str, str]] = {}
for _star_id, _name in STAR_DISPLAY_NAMES.items():
    NAME_TO_ID[_name] = _star_id
    NAME_TO_ID[_name.lower()] = _star_id
for _star_id, _aliases in STAR_ALIASES.items():
    for _alias in _aliases:
        NAME_TO_ID[_alias] = _star_id
        NAME_TO_ID[_alias.lower()] = _star_id

DOMAIN_AUTHORITY: Final[str] = "authority"
DOMAIN_CAREER: Final[str] = "career"
DOMAIN_WEALTH: Final[str] = "wealth"
DOMAIN_RELATIONSHIP: Final[str] = "relationship"
DOMAIN_CHILDREN: Final[str] = "children"
DOMAIN_HEALTH: Final[str] = "health"
DOMAIN_CREATIVE: Final[str] = "creative"
DOMAIN_ACADEMIC: Final[str] = "academic"
DOMAIN_TRAVEL: Final[str] = "travel"
DOMAIN_SPIRITUAL: Final[str] = "spiritual"
DOMAIN_PUBLIC: Final[str] = "public_reputation"
DOMAIN_PROTECTION: Final[str] = "protection"
DOMAIN_RISK: Final[str] = "risk"

SUPPORTED_BANDS: Final[frozenset[str]] = frozenset(
    {"high", "very_strong", "strong", "moderate", "present"}
)
LOW_BANDS: Final[frozenset[str]] = frozenset(
    {"low", "weak", "absent", "blocked", "very_weak"}
)
UNRESOLVED_BANDS: Final[frozenset[str]] = frozenset(
    {"unresolved", "not_available", "not_evaluated", ""}
)

STAR_CATEGORIES: Final[Mapping[str, tuple[str, ...]]] = {
    ID_TIAN_YI: ("support", "protection"),
    ID_WEN_CHANG: ("academic",),
    ID_LU_SHEN: ("wealth",),
    ID_HONG_LUAN: ("relationship",),
    ID_TIAN_XI: ("relationship",),
    ID_HUA_GAI: ("creative", "academic"),
    ID_YANG_REN: ("risk",),
    ID_TIAN_DE: ("protection", "support"),
    ID_YUE_DE: ("protection", "support"),
    ID_GUO_YIN: ("authority",),
    ID_HOC_DUONG: ("academic",),
    ID_THAI_CUC: ("creative",),
    ID_HAM_TRI: ("relationship",),
    ID_GIAI_THAN: ("protection",),
    ID_KHONG_VONG: ("risk",),
    ID_CO_THAN: ("risk",),
    ID_QUA_TU: ("risk",),
}

STAR_REQUIRED_DOMAINS: Final[Mapping[str, tuple[str, ...]]] = {
    ID_TIAN_YI: (DOMAIN_AUTHORITY, DOMAIN_CAREER),
    ID_WEN_CHANG: (DOMAIN_ACADEMIC,),
    ID_LU_SHEN: (DOMAIN_WEALTH,),
    ID_HONG_LUAN: (DOMAIN_RELATIONSHIP,),
    ID_TIAN_XI: (DOMAIN_RELATIONSHIP,),
    ID_HUA_GAI: (DOMAIN_CREATIVE, DOMAIN_ACADEMIC),
    ID_YANG_REN: (DOMAIN_RISK, DOMAIN_AUTHORITY),
    ID_TIAN_DE: (DOMAIN_AUTHORITY, DOMAIN_CAREER, DOMAIN_WEALTH, DOMAIN_ACADEMIC, DOMAIN_CREATIVE),
    ID_YUE_DE: (DOMAIN_AUTHORITY, DOMAIN_CAREER, DOMAIN_WEALTH, DOMAIN_ACADEMIC, DOMAIN_CREATIVE),
    ID_GUO_YIN: (DOMAIN_AUTHORITY, DOMAIN_CAREER),
    ID_HOC_DUONG: (DOMAIN_ACADEMIC,),
    ID_THAI_CUC: (DOMAIN_CREATIVE,),
    ID_HAM_TRI: (DOMAIN_RELATIONSHIP,),
    ID_GIAI_THAN: (DOMAIN_AUTHORITY, DOMAIN_CAREER, DOMAIN_WEALTH, DOMAIN_ACADEMIC, DOMAIN_CREATIVE),
    ID_KHONG_VONG: (DOMAIN_RISK,),
    ID_CO_THAN: (DOMAIN_RISK, DOMAIN_RELATIONSHIP),
    ID_QUA_TU: (DOMAIN_RISK, DOMAIN_RELATIONSHIP),
}

WARNING_STAR_IDS: Final[frozenset[str]] = frozenset(
    {ID_YANG_REN, ID_KHONG_VONG, ID_CO_THAN, ID_QUA_TU}
)

CLUSTER_AUTHORITY: Final[str] = "authority"
CLUSTER_ACADEMIC: Final[str] = "academic"
CLUSTER_CREATIVE: Final[str] = "creative"
CLUSTER_RELATIONSHIP: Final[str] = "relationship"
CLUSTER_CHILDREN: Final[str] = "children"
CLUSTER_HEALTH: Final[str] = "health"
CLUSTER_PROTECTION: Final[str] = "protection"
CLUSTER_TRAVEL: Final[str] = "travel"
CLUSTER_SPIRITUAL: Final[str] = "spiritual"
CLUSTER_WEALTH: Final[str] = "wealth"
CLUSTER_PUBLIC: Final[str] = "public_reputation"
CLUSTER_RISK: Final[str] = "risk"

CANONICAL_CLUSTER_IDS: Final[tuple[str, ...]] = (
    CLUSTER_AUTHORITY,
    CLUSTER_ACADEMIC,
    CLUSTER_CREATIVE,
    CLUSTER_RELATIONSHIP,
    CLUSTER_CHILDREN,
    CLUSTER_HEALTH,
    CLUSTER_PROTECTION,
    CLUSTER_TRAVEL,
    CLUSTER_SPIRITUAL,
    CLUSTER_WEALTH,
    CLUSTER_PUBLIC,
    CLUSTER_RISK,
)

CLUSTER_CANDIDATES: Final[Mapping[str, tuple[str, ...]]] = {
    CLUSTER_AUTHORITY: (ID_GUO_YIN, ID_TIAN_YI, ID_TIAN_DE, ID_YUE_DE),
    CLUSTER_ACADEMIC: (ID_WEN_CHANG, ID_HUA_GAI, ID_HOC_DUONG),
    CLUSTER_CREATIVE: (ID_HUA_GAI, ID_WEN_CHANG, ID_THAI_CUC),
    CLUSTER_RELATIONSHIP: (ID_HONG_LUAN, ID_TIAN_XI, ID_HAM_TRI),
    CLUSTER_CHILDREN: (),
    CLUSTER_HEALTH: (ID_KHONG_VONG, ID_YANG_REN),
    CLUSTER_PROTECTION: (ID_TIAN_DE, ID_YUE_DE, ID_TIAN_YI, ID_GIAI_THAN),
    CLUSTER_TRAVEL: (),
    CLUSTER_SPIRITUAL: (ID_HUA_GAI,),
    CLUSTER_WEALTH: (ID_LU_SHEN,),
    CLUSTER_PUBLIC: (ID_WEN_CHANG, ID_GUO_YIN),
    CLUSTER_RISK: (ID_KHONG_VONG, ID_CO_THAN, ID_QUA_TU, ID_YANG_REN),
}

CLUSTER_REQUIRED_DOMAINS: Final[Mapping[str, tuple[str, ...]]] = {
    CLUSTER_AUTHORITY: (DOMAIN_AUTHORITY, DOMAIN_CAREER),
    CLUSTER_ACADEMIC: (DOMAIN_ACADEMIC,),
    CLUSTER_CREATIVE: (DOMAIN_CREATIVE, DOMAIN_ACADEMIC),
    CLUSTER_RELATIONSHIP: (DOMAIN_RELATIONSHIP,),
    CLUSTER_CHILDREN: (DOMAIN_CHILDREN,),
    CLUSTER_HEALTH: (DOMAIN_HEALTH, DOMAIN_RISK),
    CLUSTER_PROTECTION: (DOMAIN_AUTHORITY, DOMAIN_CAREER, DOMAIN_WEALTH, DOMAIN_ACADEMIC, DOMAIN_CREATIVE),
    CLUSTER_TRAVEL: (DOMAIN_TRAVEL,),
    CLUSTER_SPIRITUAL: (DOMAIN_ACADEMIC, DOMAIN_CREATIVE),
    CLUSTER_WEALTH: (DOMAIN_WEALTH,),
    CLUSTER_PUBLIC: (DOMAIN_AUTHORITY, DOMAIN_ACADEMIC, DOMAIN_PUBLIC),
    CLUSTER_RISK: (DOMAIN_RISK,),
}

CLUSTER_DISPLAY_NAMES: Final[Mapping[str, str]] = {
    CLUSTER_AUTHORITY: "Quyền hạn",
    CLUSTER_ACADEMIC: "Học thuật",
    CLUSTER_CREATIVE: "Sáng tạo",
    CLUSTER_RELATIONSHIP: "Quan hệ",
    CLUSTER_CHILDREN: "Con cái",
    CLUSTER_HEALTH: "Sức khỏe",
    CLUSTER_PROTECTION: "Bảo hộ",
    CLUSTER_TRAVEL: "Di chuyển",
    CLUSTER_SPIRITUAL: "Nội tâm",
    CLUSTER_WEALTH: "Tài",
    CLUSTER_PUBLIC: "Danh tiếng",
    CLUSTER_RISK: "Cảnh báo",
}

CATEGORY_DISPLAY_NAMES: Final[Mapping[str, str]] = {
    "support": "Hỗ trợ",
    "authority": "Quyền hạn",
    "academic": "Học thuật",
    "creative": "Sáng tạo",
    "relationship": "Quan hệ",
    "children": "Con cái",
    "health": "Sức khỏe",
    "travel": "Di chuyển",
    "risk": "Cảnh báo",
    "protection": "Bảo hộ",
    "spiritual": "Nội tâm",
    "wealth": "Tài",
    "public_reputation": "Danh tiếng",
}

CONDITION_MC01_NOT_BOUND: Final[str] = "mc01:not_bound"
CONDITION_DETECTED: Final[str] = "detected:true"
CONDITION_NOT_DETECTED: Final[str] = "detected:false"
WARNING_NO_STRUCTURAL_PROMOTION: Final[str] = "warning:no_structural_promotion"
WARNING_UNKNOWN_STAR: Final[str] = "warning:unknown_star_id"

USABLE_MODIFIERS: Final[frozenset[str]] = frozenset(
    {"applied", "weak_support", "qualified", "warning"}
)
APPLIED_MODIFIERS: Final[frozenset[str]] = frozenset({"applied"})
BLOCKED_MODIFIERS: Final[frozenset[str]] = frozenset({"blocked", "inactive", "unresolved"})

STRENGTH_RANK: Final[Mapping[str, int]] = {
    "very_strong": 5,
    "strong": 4,
    "moderate": 3,
    "weak": 2,
    "conditional": 1,
    "none": 0,
    "unresolved": 0,
}

DOMAIN_RANK: Final[Mapping[str, int]] = {
    "high": 3,
    "very_strong": 3,
    "strong": 3,
    "moderate": 2,
    "present": 2,
    "low": 0,
    "weak": 0,
    "absent": 0,
    "blocked": 0,
    "unresolved": 0,
    "not_available": 0,
}
