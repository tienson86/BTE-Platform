"""LANG-01 Language Pack schema and isolation tests. No prose-quality assertions."""

from __future__ import annotations

import ast
from dataclasses import replace
from pathlib import Path

import pytest

from consulting.language.bindings.marriage import R02_SEMANTIC_TO_LANGUAGE_KEY, language_key_for
from consulting.language.catalog import get_entry, load_validated_marriage_catalog
from consulting.language.exceptions import LanguageCatalogError, LanguagePackNotIntegratedError
from consulting.language.loader import load_schema
from consulting.language.models import LanguageCatalog, LanguageCatalogFile, LanguageEntry
from consulting.language.renderer import render_for_live_tv01
from consulting.language.selector import select_wording
from consulting.language.validator import validate_catalog
from consulting.language.versions import (
    LANGUAGE_PACK_VERSION,
    MARRIAGE_CATALOG_VERSION,
    PLACEHOLDER_TOKEN,
    SCHEMA_VERSION,
)

ROOT = Path(__file__).resolve().parents[2]
MARRIAGE_ROOT = ROOT / "consulting" / "marriage"


def test_schema_and_marriage_catalog_load() -> None:
    """YAML schema and marriage catalogs load with required versions."""
    schema = load_schema()
    assert schema["schema_version"] == SCHEMA_VERSION
    assert schema["placeholder_token"] == PLACEHOLDER_TOKEN
    catalog = load_validated_marriage_catalog()
    assert catalog.language_pack_version == LANGUAGE_PACK_VERSION
    assert catalog.catalog_version == MARRIAGE_CATALOG_VERSION
    assert catalog.module == "marriage"
    assert len(catalog.files) == 6
    assert "marriage.q1.mixed" in catalog.entries_by_key
    assert "marriage.q5.insufficient" in catalog.entries_by_key
    assert "marriage.q6.can_progress" in catalog.entries_by_key


def test_duplicate_language_key_is_rejected() -> None:
    """Duplicate language_key across the catalog is a load/validation error."""
    catalog = load_validated_marriage_catalog()
    entry = get_entry(catalog, "marriage.q1.mixed")
    clone_file = LanguageCatalogFile(
        path="dup.yaml",
        module="marriage",
        question_id="Q1",
        catalog_version=catalog.catalog_version,
        module_language_version=catalog.module_language_version,
        schema_version=SCHEMA_VERSION,
        status="skeleton",
        entries=[entry],
    )
    broken = LanguageCatalog(
        module=catalog.module,
        catalog_version=catalog.catalog_version,
        module_language_version=catalog.module_language_version,
        language_pack_version=catalog.language_pack_version,
        files=[*catalog.files, clone_file],
        entries_by_key=catalog.entries_by_key,
    )
    with pytest.raises(LanguageCatalogError, match="duplicate_language_key"):
        validate_catalog(broken)


def test_missing_required_field_is_rejected() -> None:
    """Required Language Entry fields cannot be empty."""
    catalog = load_validated_marriage_catalog()
    entry = replace(get_entry(catalog, "marriage.q1.mixed"), semantic_state="")
    _replace_entry(catalog, "marriage.q1.mixed", entry)
    with pytest.raises(LanguageCatalogError, match="missing_required"):
        validate_catalog(catalog)


def test_variant_selection_is_deterministic() -> None:
    """Same semantic signature and catalog version select the same variant."""
    catalog = load_validated_marriage_catalog()
    entry = get_entry(catalog, "marriage.q1.mixed")
    first = select_wording(
        entry,
        semantic_signature="Q1|average|conflict=present",
        catalog_version=catalog.catalog_version,
    )
    second = select_wording(
        entry,
        semantic_signature="Q1|average|conflict=present",
        catalog_version=catalog.catalog_version,
    )
    assert first.variant_id == second.variant_id
    assert first.variant_id in {"v1", "v2"}
    assert first.headline == PLACEHOLDER_TOKEN


def test_forbidden_term_is_rejected() -> None:
    """Banned customer phrases fail validation even on a single field."""
    catalog = load_validated_marriage_catalog()
    entry = replace(
        get_entry(catalog, "marriage.q4.pressured"),
        status="draft",
        headline="chắc chắn ly hôn",
    )
    _replace_entry(catalog, "marriage.q4.pressured", entry)
    with pytest.raises(LanguageCatalogError, match="forbidden_term"):
        validate_catalog(catalog)


def test_module_isolation_rejects_foreign_module_entry() -> None:
    """A business entry cannot live in a marriage catalog file."""
    catalog = load_validated_marriage_catalog()
    entry = replace(
        get_entry(catalog, "marriage.q1.mixed"),
        language_key="business.q1.mixed",
        module="business",
        question_id="Q1",
    )
    _replace_entry(catalog, "marriage.q1.mixed", entry)
    with pytest.raises(LanguageCatalogError, match="module_isolation"):
        validate_catalog(catalog)


def test_r02_binding_keys_exist_in_catalog() -> None:
    """Seam map points at catalog keys. It does not rewrite Assessment."""
    catalog = load_validated_marriage_catalog()
    for language_key in R02_SEMANTIC_TO_LANGUAGE_KEY.values():
        assert language_key in catalog.entries_by_key
    assert language_key_for("Q1", "average") == "marriage.q1.mixed"
    assert language_key_for("Q5", "insufficient") == "marriage.q5.insufficient"


def test_live_renderer_is_not_integrated() -> None:
    """LANG-01 must not replace live TV-01 wording."""
    catalog = load_validated_marriage_catalog()
    entry = get_entry(catalog, "marriage.q1.mixed")
    selected = select_wording(
        entry,
        semantic_signature="Q1|average",
        catalog_version=catalog.catalog_version,
    )
    with pytest.raises(LanguagePackNotIntegratedError):
        render_for_live_tv01(entry, selected)


def test_language_pack_not_imported_by_tv01_runtime() -> None:
    """Marriage Decision / Assessment / Narrative must not import Language Pack yet."""
    leaked: list[str] = []
    for path in MARRIAGE_ROOT.rglob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                names = [alias.name for alias in node.names]
            elif isinstance(node, ast.ImportFrom) and node.module:
                names = [node.module]
            else:
                continue
            if any(name == "consulting.language" or name.startswith("consulting.language.") for name in names):
                leaked.append(str(path.relative_to(ROOT)))
    assert leaked == []


def _replace_entry(catalog: LanguageCatalog, original_key: str, entry: LanguageEntry) -> None:
    """Swap one in-memory catalog entry for a validation fixture."""
    for file in catalog.files:
        for index, existing in enumerate(file.entries):
            if existing.language_key == original_key:
                file.entries[index] = entry
                return
    raise AssertionError(f"entry_not_found:{original_key}")
