from __future__ import annotations


def eq(a, b):
    return a == b


def ne(a, b):
    return a != b


def gt(a, b):
    return a > b


def gte(a, b):
    return a >= b


def lt(a, b):
    return a < b


def lte(a, b):
    return a <= b


def contains(a, b):
    return b in a


def starts_with(a, b):
    return str(a).startswith(str(b))


def ends_with(a, b):
    return str(a).endswith(str(b))


def exists(a):
    return a is not None


OPERATORS = {
    "eq": eq,
    "ne": ne,
    "gt": gt,
    "gte": gte,
    "lt": lt,
    "lte": lte,
    "contains": contains,
    "starts_with": starts_with,
    "ends_with": ends_with,
    "exists": exists,
}
