"""Product Context Engine — resolve delivery context from customer context."""

from __future__ import annotations

from applications.production.product_context.feature_filter import (
    safety_blocks_for,
    select_action_profile,
    select_features,
    select_language_profile,
    select_tone,
)
from applications.production.product_context.life_stage import resolve_life_stage
from applications.production.product_context.models import (
    LifeStage,
    ProductContextInput,
    ProductContextResult,
    PurchasePackage,
    ReaderRole,
)

ENGINE_VERSION = "1.1.0"


class ProductContextEngine:
    """Determine how validated consulting should be delivered."""

    def resolve(self, data: ProductContextInput) -> ProductContextResult:
        """Resolve ProductContextResult from canonical input."""
        life_stage, age = resolve_life_stage(data)
        reader_role = data.reader_role
        if reader_role == ReaderRole.UNKNOWN and life_stage == LifeStage.CHILD:
            # Default audience for child charts: parent.
            reader_role = ReaderRole.PARENT

        visible, hidden, blocked = select_features(
            life_stage=life_stage,
            reader_role=reader_role,
            purchase_package=data.purchase_package,
            report_type=data.report_type,
        )
        language_profile = select_language_profile(
            life_stage=life_stage,
            reader_role=reader_role,
        )
        action_profile = select_action_profile(
            life_stage=life_stage,
            reader_role=reader_role,
        )
        tone = select_tone(language_profile=language_profile)
        safety = safety_blocks_for(life_stage=life_stage, visible=visible)

        # Adult commercial default: pass-through delivery (CASE-0001/0002 unchanged).
        pass_through = life_stage in {
            LifeStage.ADULT,
            LifeStage.MID_CAREER,
            LifeStage.YOUNG_ADULT,
        } and reader_role in {ReaderRole.SELF, ReaderRole.UNKNOWN, ReaderRole.CONSULTANT}

        if data.purchase_package == PurchasePackage.PACKAGE_A:
            pass_through = False

        return ProductContextResult(
            reader_role=reader_role,
            life_stage=life_stage,
            subject_age=age,
            language_profile=language_profile,
            visible_features=visible,
            hidden_features=hidden,
            blocked_sections=blocked,
            action_profile=action_profile,
            tone=tone,
            purchase_package=data.purchase_package,
            safety_blocks=safety,
            pass_through=pass_through,
            diagnostics={
                "engine_version": ENGINE_VERSION,
                "question_context": data.question_context,
                "customer_goal": data.customer_goal,
                "report_type": data.report_type.value,
                "language": data.language,
                "input_reader_role": data.reader_role.value,
            },
        )
