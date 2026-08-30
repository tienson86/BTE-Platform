"""Runtime Sentence Library tests (N-IMP-07C)."""

from __future__ import annotations

import ast
from pathlib import Path
from typing import Any

from engines.narrative_v2.communication import CommunicationEngine
from engines.narrative_v2.conversation import ConversationComposer
from engines.narrative_v2.evidence import EvidenceBuilder
from engines.narrative_v2.interpretation import InterpretationBuilder
from engines.narrative_v2.knowledge import KnowledgeResolver
from engines.narrative_v2.language import (
    SENTENCE_LIBRARY_VERSION,
    SentenceAsset,
    SentenceAssetValidator,
    SentenceLibrary,
    SentenceReference,
    SentenceRegistry,
    SentenceSelector,
)
from engines.narrative_v2.language.language_asset_status import STATUS_APPROVED, STATUS_DRAFT
from engines.narrative_v2.reasoning import ReasoningBuilder
from engines.narrative_v2.rewrite import RewriteEngine
from engines.narrative_v2.rewrite.language_profile import LanguageProfile

PROJECT_ROOT = Path(__file__).resolve().parents[2]
LANGUAGE_DIR = PROJECT_ROOT / "engines" / "narrative_v2" / "language"
REWRITE_SELECTOR = PROJECT_ROOT / "engines" / "narrative_v2" / "rewrite" / "sentence_selector.py"

FORBIDDEN_CLAIMS: tuple[str, ...] = (
    "chắc chắn thành công",
    "đại cát",
    "rất may mắn",
    "tình duyên sẽ tốt",
    "nên dùng màu đỏ",
    "nên đi hướng Nam",
    "nên mở rộng kinh doanh",
)

SHORTHAND: tuple[str, ...] = (
    "chỗ dưỡng",
    "việc cần nền",
    "ủ và học có khung",
    "kênh thoát",
    "chế được giữ phép",
    "nền lực",
    "chịu tải",
)


def _imported_modules(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            names.add(node.module)
    return names


def _asset(**overrides: object) -> SentenceAsset:
    payload: dict[str, object] = {
        "sentence_id": "sentence.test.meaning.001",
        "semantic_key": "core.pattern_context",
        "domain": "pattern",
        "category": "meaning",
        "meaning_key": "knowledge.pattern.chinh_an",
        "text": "Bạn thường làm việc tốt hơn khi có chỗ dựa ổn định.",
        "locale": "vi",
        "audience": "customer",
        "style": "consultant",
        "status": STATUS_APPROVED,
        "priority": 1,
        "source_knowledge_ids": ("knowledge.pattern.chinh_an",),
        "references": (
            SentenceReference(
                knowledge_id="knowledge.pattern.chinh_an",
                source_path="knowledge/interpretation/domains/pattern/chinh_an.json",
            ),
        ),
        "version": SENTENCE_LIBRARY_VERSION,
        "metadata": (("source_meaning", "Có chỗ dưỡng."),),
    }
    payload.update(overrides)
    return SentenceAsset(**payload)  # type: ignore[arg-type]


def _pipeline(case_0001_canonical: dict[str, Any]) -> tuple[object, object, object, object]:
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge, reasoning, evidence)
    interpretation = InterpretationBuilder().build(rewrite)
    conversation = ConversationComposer().compose(rewrite, interpretation)
    consulting = CommunicationEngine().style(conversation)
    return rewrite, interpretation, conversation, consulting


def test_la1_approved_sentence_asset_loads() -> None:
    assets = SentenceRegistry().assets()
    approved = [item for item in assets if item.status == STATUS_APPROVED]
    assert approved
    assert SentenceRegistry().version() == SENTENCE_LIBRARY_VERSION
    outcome = SentenceAssetValidator().validate(approved[0])
    assert outcome.passed is True


def test_la2_draft_asset_does_not_resolve() -> None:
    selected = SentenceLibrary().select(
        "core.pattern_context",
        category="meaning",
        domain="pattern",
        meaning_key="knowledge.pattern.chinh_an",
    )
    assert selected is not None
    assert selected.status == STATUS_APPROVED
    assert selected.sentence_id == "sentence.pattern.chinh_an.meaning.001"
    draft = [
        item
        for item in SentenceRegistry().assets()
        if item.sentence_id == "sentence.pattern.chinh_an.meaning.draft"
    ]
    assert draft
    assert draft[0].status == STATUS_DRAFT


def test_la3_stable_ids() -> None:
    first = tuple(item.sentence_id for item in SentenceRegistry().assets())
    second = tuple(item.sentence_id for item in SentenceRegistry().assets())
    assert first == second
    for sentence_id in first:
        assert sentence_id.startswith("sentence.")


def test_la4_deterministic_selection() -> None:
    selector = SentenceSelector()
    first = selector.select("core.pattern_context", category="meaning", domain="pattern")
    second = selector.select("core.pattern_context", category="meaning", domain="pattern")
    assert first is not None
    assert first == second


def test_la5_semantic_key_exact_matching() -> None:
    selected = SentenceLibrary().select(
        "core.pattern_context",
        category="meaning",
        domain="strength",
        meaning_key="knowledge.strength.strong",
    )
    assert selected is not None
    assert selected.meaning_key == "knowledge.strength.strong"


def test_la6_no_fuzzy_matching() -> None:
    assert (
        SentenceLibrary().select("core.pattern_contex", category="meaning", domain="pattern")
        is None
    )
    assert (
        SentenceLibrary().select(
            "core.pattern_context",
            category="meaning",
            domain="pattern",
            meaning_key="knowledge.pattern.chinh_an_extra",
        )
        is None
    )


def test_la7_source_knowledge_trace_required() -> None:
    outcome = SentenceAssetValidator().validate(
        _asset(source_knowledge_ids=(), references=())
    )
    assert outcome.passed is False
    assert "source Knowledge" in outcome.reason


def test_la8_no_unsupported_meaning() -> None:
    for claim in FORBIDDEN_CLAIMS:
        outcome = SentenceAssetValidator().validate(
            _asset(text=f"Bạn {claim} trong công việc.")
        )
        assert outcome.passed is False


def test_la9_no_prediction() -> None:
    outcome = SentenceAssetValidator().validate(
        _asset(text="Bạn chắc chắn sẽ giàu.")
    )
    assert outcome.passed is False


def test_la10_no_action() -> None:
    outcome = SentenceAssetValidator().validate(
        _asset(text="Bạn nên mở rộng kinh doanh ngay.")
    )
    assert outcome.passed is False
    outcome = SentenceAssetValidator().validate(_asset(category="action", text="Bạn nên."))
    assert outcome.passed is False


def test_la11_language_standard_enforced() -> None:
    outcome = SentenceAssetValidator().validate(
        _asset(text="Đương số có chỗ dưỡng.")
    )
    assert outcome.passed is False


def test_la12_vietnamese_natural_language_rules() -> None:
    approved = [
        item
        for item in SentenceRegistry().assets()
        if item.status == STATUS_APPROVED
    ]
    blob = " ".join(item.text for item in approved)
    for token in SHORTHAND:
        assert token not in blob
    for item in approved:
        assert item.text.startswith("Bạn")
        outcome = SentenceAssetValidator().validate(item)
        assert outcome.passed is True


def test_la13_rewrite_selector_uses_approved_assets(
    case_0001_canonical: dict[str, Any],
) -> None:
    profile = LanguageProfile()
    asset = RewriteEngine()._sentences.select(
        "core.pattern_context",
        profile=profile,
        category="meaning",
        domain="pattern",
        meaning_key="knowledge.pattern.chinh_an",
    )
    assert asset is not None
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge)
    primary = rewrite.item("rewrite.pattern.chinh_an.001")
    assert primary is not None
    assert dict(primary.metadata)["sentence_source"] == "sentence_library"
    assert primary.customer_language == asset.text


def test_la14_missing_asset_remains_unresolved_or_fallback_safe(
    case_0001_canonical: dict[str, Any],
) -> None:
    assert SentenceLibrary().select("core.useful_god_context", category="meaning") is None
    evidence = EvidenceBuilder().build(case_0001_canonical)
    reasoning = ReasoningBuilder().build(evidence)
    knowledge = KnowledgeResolver().resolve(reasoning, evidence)
    rewrite = RewriteEngine().rewrite(knowledge)
    keys = {entry.semantic_key for entry in rewrite.unresolved}
    assert "core.useful_god_context" in keys
    wrapped = [
        item
        for item in rewrite.items
        if dict(item.metadata).get("sentence_source") == "address_wrap"
    ]
    assert wrapped
    for item in wrapped:
        assert item.customer_language.startswith("Bạn")


def test_la15_no_pack05_dependency() -> None:
    forbidden = "engines.narrative_engine"
    for path in LANGUAGE_DIR.glob("*.py"):
        imported = _imported_modules(path)
        assert not any(item == forbidden or item.startswith(forbidden + ".") for item in imported)
    imported = _imported_modules(REWRITE_SELECTOR)
    assert not any(item == forbidden or item.startswith(forbidden + ".") for item in imported)


def test_la16_no_portal_dependency() -> None:
    forbidden = (
        "applications.customer_portal",
        "applications.api.services.narrative_result_truth",
    )
    for path in list(LANGUAGE_DIR.glob("*.py")) + [REWRITE_SELECTOR]:
        imported = _imported_modules(path)
        for name in forbidden:
            assert not any(item == name or item.startswith(name + ".") for item in imported)


def test_la17_no_network() -> None:
    for path in LANGUAGE_DIR.glob("*.py"):
        source = path.read_text(encoding="utf-8").lower()
        for token in ("httpx", "requests", "urllib", "aiohttp"):
            assert token not in source


def test_la18_no_language_model_generation() -> None:
    for path in LANGUAGE_DIR.glob("*.py"):
        source = path.read_text(encoding="utf-8").lower()
        for token in ("openai", "anthropic", "httpx"):
            assert token not in source


def test_la19_same_input_same_sentence() -> None:
    library = SentenceLibrary()
    first = library.select(
        "core.pattern_context",
        category="meaning",
        domain="pattern",
        meaning_key="knowledge.pattern.chinh_an",
    )
    second = library.select(
        "core.pattern_context",
        category="meaning",
        domain="pattern",
        meaning_key="knowledge.pattern.chinh_an",
    )
    assert first is not None
    assert first == second


def test_la20_case_0001_language_improves_without_meaning_change(
    case_0001_canonical: dict[str, Any],
) -> None:
    rewrite, interpretation, conversation, consulting = _pipeline(case_0001_canonical)
    primary = rewrite.item("rewrite.pattern.chinh_an.001")
    assert primary is not None
    assert "chỗ dưỡng" in primary.source_meaning
    assert "chỗ dưỡng" not in primary.customer_language
    assert interpretation.meaning == primary.customer_language
    assert conversation.meaning == interpretation.meaning
    blob = consulting.flow
    for token in ("chỗ dưỡng", "ủ và học có khung", "kênh thoát", "nền lực", "chịu tải"):
        assert token not in blob
    assert "chắc chắn thành công" not in blob
    assert "Bạn nên" not in blob
