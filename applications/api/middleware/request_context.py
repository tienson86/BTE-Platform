"""Compatibility shim — prefer ``middleware`` package register_middleware."""

from applications.api.middleware import register_middleware

__all__ = ["register_middleware"]
