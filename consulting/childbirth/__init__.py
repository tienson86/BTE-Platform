"""Childbirth consulting module."""

from consulting.childbirth.service import (
    CHILDBIRTH_MODULE_VERSION,
    analyze_childbirth_plan,
    evaluate_childbirth_years,
)

__all__ = [
    "CHILDBIRTH_MODULE_VERSION",
    "analyze_childbirth_plan",
    "evaluate_childbirth_years",
]
