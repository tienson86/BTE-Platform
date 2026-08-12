"""Product Context Engine V1.0 — customer context orchestration."""

from applications.production.product_context.delivery import ContextDeliveryAdapter
from applications.production.product_context.engine import ProductContextEngine
from applications.production.product_context.models import (
    ActionProfile,
    LanguageProfile,
    LifeStage,
    ProductContextInput,
    ProductContextResult,
    PurchasePackage,
    ReaderRole,
    ReportType,
)

__all__ = [
    "ActionProfile",
    "ContextDeliveryAdapter",
    "LanguageProfile",
    "LifeStage",
    "ProductContextEngine",
    "ProductContextInput",
    "ProductContextResult",
    "PurchasePackage",
    "ReaderRole",
    "ReportType",
]
