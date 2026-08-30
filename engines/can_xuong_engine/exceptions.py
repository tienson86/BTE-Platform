"""Cân Xương Đoán Mệnh (稱骨) engine exceptions."""

from __future__ import annotations


class CanXuongEngineError(Exception):
    """Base error for Cân Xương Engine."""


class CanXuongLookupError(CanXuongEngineError):
    """Required lookup row is missing from the Cân Xương tables."""
