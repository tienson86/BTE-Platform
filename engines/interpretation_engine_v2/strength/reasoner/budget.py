"""Frozen narrative budget caps."""

from __future__ import annotations

CUSTOMER_BUDGET: dict[str, tuple[int, int]] = {
    "CONCLUSION": (1, 1),
    "WHY": (2, 4),
    "MEANING": (1, 1),
    "ADVANTAGE": (2, 2),
    "CHALLENGE": (2, 2),
    "PERSONALITY": (0, 0),
    "CAREER": (0, 1),
    "WEALTH": (0, 0),
    "MARRIAGE": (0, 1),
    "HEALTH": (0, 1),
    "LUCK": (0, 0),
    "RECOMMENDATION": (2, 3),
    "WARNING": (0, 1),
    "SUMMARY": (5, 8),
}

PRIORITY_SCORE = {"CORE": 100, "HIGH": 80, "NORMAL": 60, "LOW": 40}
VALUE_SCORE = {"CRITICAL": 40, "HIGH": 30, "MEDIUM": 20, "LOW": 10}
WEIGHT_SCORE = {"CORE": 15, "SUPPORTING": 5, "OPTIONAL": 0, "DETAIL": 0}
SPECIFICITY_SCORE = {"CONTEXTUAL": 20, "GENERIC": 0, "CLASS_LEVEL": 10, "CAUSE_SPECIFIC": 25}

# Representative preference within duplicate clusters for CASE-0001 policy.
CLUSTER_REPRESENTATIVES: dict[str, str] = {
    "DUP-STR-FULL_TANK": "IK-STR-MEAN-0006",
    "DUP-STR-CARRY_LOAD": "IK-STR-ADV-0013",
    "DUP-STR-ENDURANCE_AS_PROOF": "IK-STR-CHAL-0010",
    "DUP-STR-BATTERY": "IK-STR-HEA-0010",
}

CLUSTER_SECTION_OWNER: dict[str, str] = {
    "DUP-STR-FULL_TANK": "MEANING",
    "DUP-STR-CARRY_LOAD": "ADVANTAGE",
}

CLUSTER_REPRESENTATIVES_REC: dict[str, str] = {
    "DUP-STR-ENDURANCE_AS_PROOF": "IK-STR-REC-0038",
}

BLOCKED_CLUSTER_SECTION: set[tuple[str, str]] = {
    ("DUP-STR-BATTERY", "CHALLENGE"),
    ("DUP-STR-FULL_TANK", "ADVANTAGE"),
    ("DUP-STR-CARRY_LOAD", "MEANING"),
    ("DUP-STR-ENDURANCE_AS_PROOF", "MEANING"),
    ("DUP-STR-ENDURANCE_AS_PROOF", "ADVANTAGE"),
}

WHY_MANDATORY_CONTROL = "IK-STR-CAUS-0016"
WHY_SEASON_UNIT = "IK-STR-CAUS-0002"
