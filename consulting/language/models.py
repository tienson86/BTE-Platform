"""Language Pack models. Wording objects. Not Decision. Not Assessment."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class LanguageFactTemplate:
    """One controlled supporting-fact or limitation template."""

    id: str
    template: str
    status: str = "placeholder"
    source_fact: str | None = None
    slots: list[str] = field(default_factory=list)


@dataclass(slots=True)
class LanguageVariant:
    """One approved wording variant for a language_key."""

    id: str
    headline: str
    meaning: str = ""
    status: str = "placeholder"


@dataclass(slots=True)
class LanguageEntry:
    """One catalog entry. Semantic identity plus optional wording slots."""

    language_key: str
    module: str
    question_id: str
    semantic_state: str
    version: str
    status: str
    audience: str = "customer"
    tone: str = "professional_warm"
    headline: str = ""
    meaning: str = ""
    plain_customer_text: str = ""
    technical_explanation: str = ""
    supporting_fact_templates: list[LanguageFactTemplate] = field(default_factory=list)
    limitation_templates: list[LanguageFactTemplate] = field(default_factory=list)
    main_risk_templates: list[LanguageFactTemplate] = field(default_factory=list)
    main_rescue_templates: list[LanguageFactTemplate] = field(default_factory=list)
    closing: str = ""
    variants: list[LanguageVariant] = field(default_factory=list)
    forbidden_terms: list[str] = field(default_factory=list)
    slots: list[str] = field(default_factory=list)


@dataclass(slots=True)
class LanguageCatalogFile:
    """One YAML catalog file for a single question."""

    path: str
    module: str
    question_id: str
    catalog_version: str
    module_language_version: str
    schema_version: str
    status: str
    entries: list[LanguageEntry]


@dataclass(slots=True)
class LanguageCatalog:
    """Loaded Language Pack catalog for one module."""

    module: str
    catalog_version: str
    module_language_version: str
    language_pack_version: str
    files: list[LanguageCatalogFile]
    entries_by_key: dict[str, LanguageEntry]


@dataclass(slots=True)
class SelectedWording:
    """Deterministic wording selection. Still placeholder in LANG-01."""

    language_key: str
    variant_id: str
    headline: str
    meaning: str
    catalog_version: str
    entry_version: str


@dataclass(slots=True)
class LanguageCardWording:
    """Rendered Assessment Card wording. Not a Decision and not an Assessment."""

    question_id: str
    question: str
    language_key: str
    headline: str
    meaning: str
    supporting_facts: list[str]
    limitations: list[str]
    closing: str
    technical_explanation: str
    variant_id: str
    confidence: str
    fallback: bool = False
    quick_guidance: str = ""
    quick_guidance_recommendation_id: str = ""
    quick_guidance_action_type: str = ""
    fact_source_keys: list[str] = field(default_factory=list)
