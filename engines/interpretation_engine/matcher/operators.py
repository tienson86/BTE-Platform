"""
BTE Platform
=============================

Interpretation Engine

Operators

Định nghĩa toàn bộ toán tử dùng trong Rule Engine.

Author : BTE Project
Version : 1.0.0
"""

from __future__ import annotations

import re
from collections.abc import Iterable
from typing import Any


# ==========================================================
# Helper
# ==========================================================

def _is_iterable(value: Any) -> bool:
    """
    Kiểm tra đối tượng có thể lặp nhưng không phải chuỗi.
    """
    return (
        isinstance(value, Iterable)
        and not isinstance(value, (str, bytes))
    )


# ==========================================================
# Comparison
# ==========================================================

def eq(left: Any, right: Any) -> bool:
    return left == right


def ne(left: Any, right: Any) -> bool:
    return left != right


def gt(left: Any, right: Any) -> bool:
    return left > right


def gte(left: Any, right: Any) -> bool:
    return left >= right


def lt(left: Any, right: Any) -> bool:
    return left < right


def lte(left: Any, right: Any) -> bool:
    return left <= right


# ==========================================================
# Collection
# ==========================================================

def contains(left: Any, right: Any) -> bool:

    if left is None:
        return False

    return right in left


def not_contains(left: Any, right: Any) -> bool:

    return not contains(left, right)


def in_(left: Any, right: Any) -> bool:

    if right is None:
        return False

    return left in right


def not_in(left: Any, right: Any) -> bool:

    return not in_(left, right)


def subset(left: Any, right: Any) -> bool:

    if not _is_iterable(left):
        return False

    if not _is_iterable(right):
        return False

    return set(left).issubset(set(right))


def superset(left: Any, right: Any) -> bool:

    if not _is_iterable(left):
        return False

    if not _is_iterable(right):
        return False

    return set(left).issuperset(set(right))


# ==========================================================
# Range
# ==========================================================

def between(value: Any, limit: tuple | list) -> bool:

    if len(limit) != 2:
        raise ValueError(
            "between yêu cầu (min,max)"
        )

    lower, upper = limit

    return lower <= value <= upper


# ==========================================================
# String
# ==========================================================

def starts_with(value: Any, prefix: str) -> bool:

    if value is None:
        return False

    return str(value).startswith(prefix)


def ends_with(value: Any, suffix: str) -> bool:

    if value is None:
        return False

    return str(value).endswith(suffix)


def regex(value: Any, pattern: str) -> bool:

    if value is None:
        return False

    return re.search(
        pattern,
        str(value),
    ) is not None


# ==========================================================
# Boolean
# ==========================================================

def is_true(value: Any, _: Any = None) -> bool:

    return bool(value) is True


def is_false(value: Any, _: Any = None) -> bool:

    return bool(value) is False


# ==========================================================
# None
# ==========================================================

def exists(value: Any, _: Any = None) -> bool:

    return value is not None


def not_exists(value: Any, _: Any = None) -> bool:

    return value is None


def empty(value: Any, _: Any = None) -> bool:

    if value is None:
        return True

    try:
        return len(value) == 0

    except Exception:
        return False


def not_empty(value: Any, _: Any = None) -> bool:

    return not empty(value)


# ==========================================================
# Logical
# ==========================================================

def all_(values: Iterable[bool], _: Any = None) -> bool:

    return all(values)


def any_(values: Iterable[bool], _: Any = None) -> bool:

    return any(values)


# ==========================================================
# Registry
# ==========================================================

OPERATORS = {

    # Comparison

    "eq": eq,
    "ne": ne,

    "gt": gt,
    "gte": gte,

    "lt": lt,
    "lte": lte,

    # Collection

    "contains": contains,
    "not_contains": not_contains,

    "in": in_,
    "not_in": not_in,

    "subset": subset,
    "superset": superset,

    # Range

    "between": between,

    # String

    "starts_with": starts_with,
    "ends_with": ends_with,
    "regex": regex,

    # Boolean

    "is_true": is_true,
    "is_false": is_false,

    # Null

    "exists": exists,
    "not_exists": not_exists,

    "empty": empty,
    "not_empty": not_empty,

    # Logic

    "all": all_,
    "any": any_,
}


# ==========================================================
# Public API
# ==========================================================

def get_operator(name: str):

    try:

        return OPERATORS[name]

    except KeyError:

        raise ValueError(
            f"Operator '{name}' không tồn tại."
        )


def has_operator(name: str) -> bool:

    return name in OPERATORS


def list_operators() -> list[str]:

    return sorted(
        OPERATORS.keys()
    )


__all__ = [
    "OPERATORS",
    "get_operator",
    "has_operator",
    "list_operators",
]
