"""Build ProductContextInput from production request options."""

from __future__ import annotations

from applications.production.models import ProductionRequest
from applications.production.product_context.models import (
    LifeStage,
    ProductContextInput,
    PurchasePackage,
    ReaderRole,
    ReportType,
)


def build_product_context_input(
    request: ProductionRequest,
    *,
    as_of_year: int | None = None,
    as_of_month: int | None = None,
    as_of_day: int | None = None,
) -> ProductContextInput:
    """Map ProductionRequest (+ options) to ProductContextInput."""
    options = dict(request.options or {})
    reader = _enum(ReaderRole, options.get("reader_role"), ReaderRole.UNKNOWN)
    package = _enum(PurchasePackage, options.get("purchase_package"), PurchasePackage.UNKNOWN)
    report_type = _enum(ReportType, options.get("report_type"), ReportType.GENERAL)
    life_stage = None
    if options.get("life_stage"):
        life_stage = _enum(LifeStage, options.get("life_stage"), None)

    subject_age = options.get("subject_age")
    if subject_age is not None:
        subject_age = int(subject_age)

    return ProductContextInput(
        subject_age=subject_age,
        birth_year=request.year,
        birth_month=request.month,
        birth_day=request.day,
        as_of_year=as_of_year or options.get("as_of_year"),
        as_of_month=as_of_month or options.get("as_of_month"),
        as_of_day=as_of_day or options.get("as_of_day"),
        life_stage=life_stage,
        reader_role=reader,
        purchase_package=package,
        question_context=str(options.get("question_context") or "GENERAL"),
        customer_goal=str(options.get("customer_goal") or ""),
        report_type=report_type,
        language=str(options.get("language") or "vi"),
        versions={"product_context": "1.0.0"},
    )


def _enum(enum_cls, value, default):
    if value is None or value == "":
        return default
    if isinstance(value, enum_cls):
        return value
    try:
        return enum_cls(str(value))
    except ValueError:
        return default
