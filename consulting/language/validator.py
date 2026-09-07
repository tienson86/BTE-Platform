"""Validate Language Pack catalogs. Schema only. No prose quality scoring."""

from __future__ import annotations

from consulting.language.exceptions import LanguageCatalogError
from consulting.language.forbidden import FORBIDDEN_CUSTOMER_TERMS
from consulting.language.models import LanguageCatalog, LanguageEntry
from consulting.language.versions import PLACEHOLDER_TOKEN, SCHEMA_VERSION


_REQUIRED = (
    "language_key",
    "module",
    "question_id",
    "semantic_state",
    "version",
    "status",
)
_ALLOWED_STATUS = {"placeholder", "draft", "approved", "frozen"}
_ALLOWED_MODULES = {"marriage", "business", "career", "child"}


def validate_catalog(catalog: LanguageCatalog) -> None:
    """Raise LanguageCatalogError if schema, uniqueness, or forbidden terms fail."""
    if catalog.language_pack_version == "":
        raise LanguageCatalogError("language_pack_version_required")
    seen: set[str] = set()
    for file in catalog.files:
        if file.schema_version != SCHEMA_VERSION:
            raise LanguageCatalogError(f"schema_version_mismatch:{file.path}")
        for entry in file.entries:
            _validate_entry(entry, file.module, file.question_id)
            if entry.language_key in seen:
                raise LanguageCatalogError(f"duplicate_language_key:{entry.language_key}")
            seen.add(entry.language_key)
    if not seen:
        raise LanguageCatalogError("catalog_empty")


def _validate_entry(entry: LanguageEntry, file_module: str, file_question: str) -> None:
    """Validate one entry against required fields and isolation rules."""
    for name in _REQUIRED:
        if not str(getattr(entry, name) or ""):
            raise LanguageCatalogError(f"missing_required:{entry.language_key}:{name}")
    if entry.module not in _ALLOWED_MODULES:
        raise LanguageCatalogError(f"unknown_module:{entry.language_key}")
    if entry.module != file_module:
        raise LanguageCatalogError(f"module_isolation:{entry.language_key}")
    if entry.question_id != file_question:
        raise LanguageCatalogError(f"question_isolation:{entry.language_key}")
    expected_prefix = f"{entry.module}.{entry.question_id.lower()}."
    if not entry.language_key.startswith(expected_prefix):
        raise LanguageCatalogError(f"language_key_prefix:{entry.language_key}")
    if entry.status not in _ALLOWED_STATUS:
        raise LanguageCatalogError(f"invalid_status:{entry.language_key}")
    if entry.status == "placeholder":
        _assert_placeholder_copy(entry)
    else:
        _assert_no_placeholder_token(entry)
    _assert_no_forbidden(entry)
    variant_ids = [item.id for item in entry.variants]
    if any(not item for item in variant_ids):
        raise LanguageCatalogError(f"variant_id_required:{entry.language_key}")
    if len(variant_ids) != len(set(variant_ids)):
        raise LanguageCatalogError(f"duplicate_variant_id:{entry.language_key}")


def _assert_placeholder_copy(entry: LanguageEntry) -> None:
    """Placeholder entries must not look like finished commercial copy."""
    texts = [
        entry.headline,
        entry.meaning,
        entry.plain_customer_text,
        entry.technical_explanation,
        entry.closing,
        *[item.headline for item in entry.variants],
        *[item.meaning for item in entry.variants],
        *[item.template for item in entry.supporting_fact_templates],
        *[item.template for item in entry.limitation_templates],
    ]
    authored = [item for item in texts if item]
    if authored and any(item != PLACEHOLDER_TOKEN for item in authored):
        raise LanguageCatalogError(f"placeholder_has_authored_copy:{entry.language_key}")


def _assert_no_placeholder_token(entry: LanguageEntry) -> None:
    """Approved catalogs must not ship Product Owner placeholder tokens."""
    texts = [
        entry.headline,
        entry.meaning,
        entry.plain_customer_text,
        entry.technical_explanation,
        entry.closing,
        *[item.headline for item in entry.variants],
        *[item.meaning for item in entry.variants],
        *[item.template for item in entry.supporting_fact_templates],
        *[item.template for item in entry.limitation_templates],
    ]
    if any(PLACEHOLDER_TOKEN in item for item in texts if item):
        raise LanguageCatalogError(f"placeholder_token_present:{entry.language_key}")


def _assert_no_forbidden(entry: LanguageEntry) -> None:
    """Reject banned customer phrases in any wording field."""
    banned = list(FORBIDDEN_CUSTOMER_TERMS)
    blob = " ".join(
        [
            entry.headline,
            entry.meaning,
            entry.plain_customer_text,
            entry.technical_explanation,
            entry.closing,
            *[item.template for item in entry.supporting_fact_templates],
            *[item.template for item in entry.limitation_templates],
            *[item.headline for item in entry.variants],
            *[item.meaning for item in entry.variants],
        ]
    ).lower()
    for term in banned:
        if term and term.lower() in blob:
            raise LanguageCatalogError(f"forbidden_term:{entry.language_key}:{term}")
