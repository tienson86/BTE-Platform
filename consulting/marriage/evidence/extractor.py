"""Canonical snapshot evidence builder. Does not score compatibility."""

from __future__ import annotations

from consulting.marriage.constants import MODULE_VERSION
from consulting.marriage.evidence.contract import MarriageEvidenceBuilder
from consulting.marriage.evidence.draft import EvidenceDraft, assign_ids
from consulting.marriage.evidence.extract_elements import extract_element_evidence
from consulting.marriage.evidence.extract_roles import extract_ten_god_evidence
from consulting.marriage.evidence.extract_secondary import extract_secondary_evidence
from consulting.marriage.evidence.extract_stems import extract_stem_branch_evidence
from consulting.marriage.evidence.extract_timing import extract_luck_evidence
from consulting.marriage.models.context import MarriageRelationshipContext
from consulting.marriage.models.evidence import MarriageEvidence
from consulting.marriage.models.versioning import MarriageVersionBundle
from consulting.marriage.policy.context import MarriagePolicyContext
from consulting.marriage.policy.versions import (
    EVIDENCE_CATALOG_VERSION,
    SCORE_MODEL_VERSION,
    policy_version_token,
)


class CanonicalEvidenceBuilder(MarriageEvidenceBuilder):
    """Extract atomic evidence from paired Canonical snapshots."""

    def build(self, context: MarriageRelationshipContext) -> list[MarriageEvidence]:
        """Create evidence atoms from a relationship context."""
        consultation_id = ""
        if context.runtime_meta is not None and context.runtime_meta.pipeline_id:
            consultation_id = context.runtime_meta.pipeline_id
        policy_context = MarriagePolicyContext(
            consultation_id=consultation_id,
            snapshot_a=context.person_a,
            snapshot_b=context.person_b,
            options=context.options,
            versions=MarriageVersionBundle(
                module_version=MODULE_VERSION,
                decision_profile_version=policy_version_token(),
                score_model_version=SCORE_MODEL_VERSION,
                rule_catalog_version=EVIDENCE_CATALOG_VERSION,
                canonical_versions=context.person_a.person.canonical_version,
            ),
            available_domains=tuple(context.available_domains),
            limitations=tuple(context.limitations),
            source_analysis_id_a=context.person_a.source_analysis_id,
            source_analysis_id_b=context.person_b.source_analysis_id,
        )
        return self.build_from_policy_context(policy_context)

    def build_from_policy_context(self, context: MarriagePolicyContext) -> list[MarriageEvidence]:
        """Extract evidence using Policy Context only."""
        drafts: list[EvidenceDraft] = []
        drafts.extend(extract_element_evidence(context))
        drafts.extend(extract_stem_branch_evidence(context))
        drafts.extend(extract_ten_god_evidence(context))
        drafts.extend(extract_luck_evidence(context))
        drafts.extend(extract_secondary_evidence(context))
        return assign_ids(drafts)
