"""Secondary reference evidence. Never used as structural core."""

from __future__ import annotations

from consulting.marriage.evidence.draft import EvidenceDraft
from consulting.marriage.evidence.snapshot_access import source_ref, snapshot_for
from consulting.marriage.models.enums import (
    EvidenceDirection,
    EvidenceSignificance,
    MarriageDomain,
    MarriageEvidenceType,
    PersonSide,
    RelationshipSubject,
)
from consulting.marriage.policy.context import MarriagePolicyContext


def extract_secondary_evidence(context: MarriagePolicyContext) -> list[EvidenceDraft]:
    """Extract Shen Sha, Cung Phi, and Nạp âm as reference-only evidence."""
    drafts: list[EvidenceDraft] = []
    if context.options.include_shen_sha is not False:
        drafts.extend(_shen_sha(context, PersonSide.A))
        drafts.extend(_shen_sha(context, PersonSide.B))
    if context.options.include_feng_shui_reference is not False:
        drafts.extend(_feng_shui(context, PersonSide.A))
        drafts.extend(_feng_shui(context, PersonSide.B))
    drafts.extend(_na_yin(context))
    return drafts


def _shen_sha(context: MarriagePolicyContext, side: PersonSide) -> list[EvidenceDraft]:
    """Copy Shen Sha names as reference evidence."""
    snapshot = snapshot_for(context, side)
    if snapshot.shen_sha is None:
        return []
    drafts: list[EvidenceDraft] = []
    for item in snapshot.shen_sha.items:
        drafts.append(
            EvidenceDraft(
                domain=MarriageDomain.FIVE_ELEMENTS,
                evidence_type=MarriageEvidenceType.SHEN_SHA_SUPPORT
                if (item.polarity or "").lower() in {"support", "positive", "auspicious"}
                else MarriageEvidenceType.SHEN_SHA_RISK
                if (item.polarity or "").lower() in {"risk", "negative", "inauspicious"}
                else MarriageEvidenceType.SHEN_SHA_SUPPORT,
                direction=EvidenceDirection.NEUTRAL,
                significance=EvidenceSignificance.MINOR,
                confidence=item.confidence if item.confidence is not None else 0.4,
                subject=RelationshipSubject.SHARED,
                source_refs=(source_ref(context, side, "shen_sha", item.name),),
                predicate=f"shen_sha_reference:{item.name}",
                scope="reference",
                rule_id="secondary.shen_sha",
                payload={"name": item.name, "side": side.value},
            )
        )
    return drafts


def _feng_shui(context: MarriagePolicyContext, side: PersonSide) -> list[EvidenceDraft]:
    """Copy Cung Phi as living-compatibility reference only."""
    snapshot = snapshot_for(context, side)
    if snapshot.feng_shui is None or not snapshot.feng_shui.cung_phi:
        return []
    cung = snapshot.feng_shui.cung_phi
    return [
        EvidenceDraft(
            domain=MarriageDomain.FAMILY,
            evidence_type=MarriageEvidenceType.FENG_SHUI_REFERENCE,
            direction=EvidenceDirection.NEUTRAL,
            significance=EvidenceSignificance.MINOR,
            confidence=0.4,
            subject=RelationshipSubject.SHARED,
            source_refs=(source_ref(context, side, "feng_shui.cung_phi", cung),),
            predicate=f"cung_phi_reference:{cung}",
            scope="reference",
            rule_id="secondary.cung_phi",
            payload={"cung_phi": cung, "side": side.value},
        )
    ]


def _na_yin(context: MarriagePolicyContext) -> list[EvidenceDraft]:
    """Record Nạp âm presence as reference. Does not apply sinh/khắc."""
    na_a = context.snapshot_a.pillars.day.na_yin
    na_b = context.snapshot_b.pillars.day.na_yin
    if not na_a or not na_b:
        return []
    return [
        EvidenceDraft(
            domain=MarriageDomain.FIVE_ELEMENTS,
            evidence_type=MarriageEvidenceType.FENG_SHUI_REFERENCE,
            direction=EvidenceDirection.NEUTRAL,
            significance=EvidenceSignificance.MINOR,
            confidence=0.3,
            subject=RelationshipSubject.SHARED,
            source_refs=(
                source_ref(context, PersonSide.A, "pillars.day.na_yin", na_a),
                source_ref(context, PersonSide.B, "pillars.day.na_yin", na_b),
            ),
            predicate="na_yin_reference",
            scope="reference",
            rule_id="secondary.na_yin",
            payload={"na_yin_a": na_a, "na_yin_b": na_b},
        )
    ]
