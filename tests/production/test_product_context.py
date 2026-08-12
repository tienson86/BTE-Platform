"""Product Context Engine V1.0 tests."""

from __future__ import annotations

import pytest

from applications.production.engine_runner import ProductionEngineRunner
from applications.production.fixtures.case_0001 import CASE_0001_REQUEST
from applications.production.fixtures.case_0002_readiness import CASE_0002_REQUEST
from applications.production.interpretation.service import MultiDomainInterpretationService
from applications.production.models import ProductionRequest
from applications.production.orchestrator import ProductionEndToEndOrchestrator
from applications.production.product_context.delivery import ContextDeliveryAdapter
from applications.production.product_context.engine import ProductContextEngine
from applications.production.product_context.models import (
    LanguageProfile,
    LifeStage,
    ProductContextInput,
    PurchasePackage,
    ReaderRole,
    ReportType,
)


@pytest.fixture(scope="module")
def engine_ctx():
    return ProductContextEngine()


def test_life_stage_child(engine_ctx) -> None:
    result = engine_ctx.resolve(
        ProductContextInput(subject_age=10, reader_role=ReaderRole.UNKNOWN)
    )
    assert result.life_stage == LifeStage.CHILD
    assert result.reader_role == ReaderRole.PARENT
    assert "career_report" in result.hidden_features
    assert "parent_guidance" in result.visible_features
    assert result.language_profile == LanguageProfile.PARENT_SUPPORT


def test_life_stage_teen(engine_ctx) -> None:
    result = engine_ctx.resolve(ProductContextInput(subject_age=15))
    assert result.life_stage == LifeStage.TEEN
    assert "career_report" in result.hidden_features


def test_life_stage_adult(engine_ctx) -> None:
    result = engine_ctx.resolve(
        ProductContextInput(subject_age=30, reader_role=ReaderRole.SELF)
    )
    assert result.life_stage == LifeStage.ADULT
    assert result.pass_through is True
    assert "career_report" in result.visible_features


def test_life_stage_senior(engine_ctx) -> None:
    result = engine_ctx.resolve(ProductContextInput(subject_age=65))
    assert result.life_stage == LifeStage.SENIOR
    assert result.language_profile == LanguageProfile.SENIOR_REFLECTION
    assert "legacy_reflection" in result.visible_features


def test_parent_reader(engine_ctx) -> None:
    result = engine_ctx.resolve(
        ProductContextInput(subject_age=30, reader_role=ReaderRole.PARENT)
    )
    assert result.language_profile == LanguageProfile.PARENT_SUPPORT
    assert result.action_profile.value == "PARENT_ACTIONS"


def test_unknown_defaults_adult(engine_ctx) -> None:
    result = engine_ctx.resolve(ProductContextInput())
    assert result.life_stage == LifeStage.ADULT


def test_package_a_hides_career_for_adult(engine_ctx) -> None:
    result = engine_ctx.resolve(
        ProductContextInput(
            subject_age=30,
            reader_role=ReaderRole.SELF,
            purchase_package=PurchasePackage.PACKAGE_A,
        )
    )
    assert "career_report" in result.hidden_features
    assert result.pass_through is False


def test_package_b_adult_keeps_career(engine_ctx) -> None:
    result = engine_ctx.resolve(
        ProductContextInput(
            subject_age=32,
            reader_role=ReaderRole.SELF,
            purchase_package=PurchasePackage.PACKAGE_B,
        )
    )
    assert "career_report" in result.visible_features


def test_package_c_adult(engine_ctx) -> None:
    result = engine_ctx.resolve(
        ProductContextInput(
            subject_age=40,
            purchase_package=PurchasePackage.PACKAGE_C,
            reader_role=ReaderRole.SELF,
        )
    )
    assert "identity_report" in result.visible_features


def test_safety_blocks_child_career_request(engine_ctx) -> None:
    result = engine_ctx.resolve(
        ProductContextInput(
            subject_age=8,
            report_type=ReportType.CAREER,
            reader_role=ReaderRole.PARENT,
        )
    )
    assert "career_report" not in result.visible_features
    assert "NO_ADULT_CAREER_DECISION" in result.safety_blocks


def test_case_0001_adult_unchanged_bodies() -> None:
    engine = ProductionEngineRunner().run(CASE_0001_REQUEST)
    composition = MultiDomainInterpretationService().compose(
        case_id="CASE-0001",
        engine_output=engine,
    )
    orch = ProductionEndToEndOrchestrator()
    result = orch.run(
        ProductionRequest(
            case_id=CASE_0001_REQUEST.case_id,
            year=CASE_0001_REQUEST.year,
            month=CASE_0001_REQUEST.month,
            day=CASE_0001_REQUEST.day,
            hour=CASE_0001_REQUEST.hour,
            minute=CASE_0001_REQUEST.minute,
            gender=CASE_0001_REQUEST.gender,
            timezone=CASE_0001_REQUEST.timezone,
            full_name=CASE_0001_REQUEST.full_name,
            birth_place=CASE_0001_REQUEST.birth_place,
            export_pdf=False,
            options={"as_of_year": 2026, "as_of_month": 8, "as_of_day": 12},
        )
    )
    assert result.success is True
    assert result.customer.section_status.career_report.value in {"AVAILABLE", "PARTIAL"}
    assert result.customer.career_report == composition.career.body
    assert result.customer.identity_report == composition.identity.body
    assert result.customer.executive_consulting == composition.executive.body
    assert result.diagnostics["product_context"]["pass_through"] is True


def test_case_0002_adult_unchanged() -> None:
    engine = ProductionEngineRunner().run(CASE_0002_REQUEST)
    composition = MultiDomainInterpretationService().compose(
        case_id="CASE-0002",
        engine_output=engine,
    )
    result = ProductionEndToEndOrchestrator().run(
        ProductionRequest(
            case_id="CASE-0002",
            year=CASE_0002_REQUEST.year,
            month=CASE_0002_REQUEST.month,
            day=CASE_0002_REQUEST.day,
            hour=CASE_0002_REQUEST.hour,
            minute=CASE_0002_REQUEST.minute,
            gender=CASE_0002_REQUEST.gender,
            timezone=CASE_0002_REQUEST.timezone,
            full_name=CASE_0002_REQUEST.full_name,
            birth_place=CASE_0002_REQUEST.birth_place,
            export_pdf=False,
            options={"as_of_year": 2026, "as_of_month": 8, "as_of_day": 12},
        )
    )
    assert result.customer.career_report == composition.career.body
    assert result.diagnostics["product_context"]["life_stage"] == "ADULT"


def test_case_0003_child_hides_career_enables_parent() -> None:
    result = ProductionEndToEndOrchestrator().run(
        ProductionRequest(
            case_id="CASE-0003",
            year=2015,
            month=2,
            day=15,
            hour=5,
            minute=30,
            gender="female",
            timezone="Asia/Ho_Chi_Minh",
            full_name="CASE-0003 Extreme Subject",
            birth_place="Hà Nội, Việt Nam",
            export_pdf=False,
            options={"as_of_year": 2026, "as_of_month": 8, "as_of_day": 12},
        )
    )
    assert result.success is True
    ctx = result.diagnostics["product_context"]
    assert ctx["life_stage"] == "CHILD"
    assert result.customer.section_status.career_report.value == "NOT_AVAILABLE"
    assert "CAREER_REPORT_HIDDEN_BY_PRODUCT_CONTEXT" in result.customer.career_report
    assert result.customer.section_status.parent_guidance.value == "AVAILABLE"
    assert "phụ huynh" in result.customer.parent_guidance.lower()
    assert "phát triển" in result.customer.identity_report.lower()
    assert "Career Decision" in result.customer.executive_consulting or (
        "career" in result.customer.executive_consulting.lower()
    )
    assert "tuần làm việc quanh kênh" not in result.customer.identity_report


def test_delivery_adapter_pass_through() -> None:
    engine = ProductionEngineRunner().run(CASE_0001_REQUEST)
    composition = MultiDomainInterpretationService().compose(
        case_id="CASE-0001",
        engine_output=engine,
    )
    ctx = ProductContextEngine().resolve(
        ProductContextInput(subject_age=40, reader_role=ReaderRole.SELF)
    )
    bundle = ContextDeliveryAdapter().apply(composition, ctx)
    assert bundle.identity.body == composition.identity.body
    assert bundle.career.body == composition.career.body
