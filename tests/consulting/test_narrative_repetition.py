"""TV1-B05 repetition control tests."""

from __future__ import annotations

from consulting.marriage.narrative.repetition import RepetitionGuard
from tests.consulting.narrative_fixtures import compose_narrative


def test_repetition_prevention_uses_semantic_ids() -> None:
    """The same finding semantic key is explained at most once."""
    decision, _, narrative = compose_narrative()
    explained: list[str] = []
    domain = next(section for section in narrative.sections if section.section_id == "domains")
    for block in domain.blocks:
        if block.block_id.startswith("finding-"):
            explained.extend(block.source_finding_ids)
    assert len(explained) == len(set(explained))
    by_id = {item.finding_id: item for item in decision.findings}
    semantic = [by_id[item].semantic_key or item for item in explained]
    assert len(semantic) == len(set(semantic))


def test_one_finding_not_repeated_as_identical_paragraphs() -> None:
    """Identical finding paragraphs must not appear in multiple sections."""
    _, _, narrative = compose_narrative()
    finding_texts = [
        block.text
        for section in narrative.sections
        for block in section.blocks
        if block.block_id.startswith("finding-")
    ]
    assert len(finding_texts) == len(set(finding_texts))
    overall = next(section for section in narrative.sections if section.section_id == "overall")
    actions = next(section for section in narrative.sections if section.section_id == "actions")
    overall_texts = {block.text for block in overall.blocks}
    action_texts = {block.text for block in actions.blocks if block.stage == "action"}
    domain = next((section for section in narrative.sections if section.section_id == "domains"), None)
    if domain is not None:
        domain_explanations = {
            block.text for block in domain.blocks if block.stage == "observation"
        }
        assert overall_texts.isdisjoint(domain_explanations)
        assert action_texts.isdisjoint(domain_explanations)


def test_identical_recommendation_intent_renders_once() -> None:
    """Merged B04 intents stay unique in the action section."""
    decision, _, narrative = compose_narrative()
    actions = next(section for section in narrative.sections if section.section_id == "actions")
    intents = [
        (block.catalog_key, tuple(block.source_recommendation_ids))
        for block in actions.blocks
        if block.source_recommendation_ids
    ]
    catalog_keys = [item[0] for item in intents]
    rec_ids = [rec_id for item in intents for rec_id in item[1]]
    assert len(rec_ids) == len(set(rec_ids))
    assert len(decision.recommendations) == len(set(item.recommendation_id for item in decision.recommendations))
    assert catalog_keys or not decision.recommendations


def test_repetition_guard_tracks_ids_not_only_strings() -> None:
    """Guard claims are keyed by semantic id."""
    guard = RepetitionGuard()
    assert guard.claim_finding("branch_clash", "F-0001") is True
    assert guard.claim_finding("branch_clash", "F-0002") is False
    assert guard.explained_finding("branch_clash", "F-0002") is True
    assert guard.claim_action("reduce_conflict", "manage_relational_tension") is True
    assert guard.claim_action("reduce_conflict", "manage_relational_tension") is False
