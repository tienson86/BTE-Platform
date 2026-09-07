"""Load Language Pack YAML. Read-only. No Decision or Assessment mutation."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from consulting.language.exceptions import LanguageCatalogError
from consulting.language.models import (
    LanguageCatalog,
    LanguageCatalogFile,
    LanguageEntry,
    LanguageFactTemplate,
    LanguageVariant,
)
from consulting.language.versions import LANGUAGE_PACK_VERSION

REPO_ROOT = Path(__file__).resolve().parents[2]
LANGUAGE_PACK_ROOT = REPO_ROOT / "knowledge" / "consulting" / "language"
MARRIAGE_CATALOG_DIR = LANGUAGE_PACK_ROOT / "marriage"
SCHEMA_PATH = LANGUAGE_PACK_ROOT / "schema.yaml"

_MARRIAGE_FILES = (
    "compatibility.yaml",
    "support.yaml",
    "personality.yaml",
    "stability.yaml",
    "children.yaml",
    "overall.yaml",
)


def load_schema() -> dict[str, Any]:
    """Load the Language Pack schema document."""
    payload = _read_yaml(SCHEMA_PATH)
    if not isinstance(payload, dict):
        raise LanguageCatalogError("schema_must_be_mapping")
    return payload


def load_marriage_catalog() -> LanguageCatalog:
    """Load TV-01 marriage YAML. Does not bind live Narrative."""
    schema = load_schema()
    files: list[LanguageCatalogFile] = []
    entries_by_key: dict[str, LanguageEntry] = {}
    catalog_version = ""
    module_language_version = ""
    for name in _MARRIAGE_FILES:
        path = MARRIAGE_CATALOG_DIR / name
        loaded = _load_file(path, schema)
        files.append(loaded)
        catalog_version = loaded.catalog_version
        module_language_version = loaded.module_language_version
        for entry in loaded.entries:
            if entry.language_key in entries_by_key:
                raise LanguageCatalogError(f"duplicate_language_key:{entry.language_key}")
            entries_by_key[entry.language_key] = entry
    return LanguageCatalog(
        module="marriage",
        catalog_version=catalog_version,
        module_language_version=module_language_version,
        language_pack_version=LANGUAGE_PACK_VERSION,
        files=files,
        entries_by_key=entries_by_key,
    )


def _load_file(path: Path, schema: dict[str, Any]) -> LanguageCatalogFile:
    """Parse one question YAML file."""
    if not path.is_file():
        raise LanguageCatalogError(f"missing_catalog_file:{path.name}")
    payload = _read_yaml(path)
    if not isinstance(payload, dict):
        raise LanguageCatalogError(f"catalog_must_be_mapping:{path.name}")
    expected_question = (schema.get("file_question_map") or {}).get(path.name)
    question_id = str(payload.get("question_id") or "")
    if expected_question and question_id != expected_question:
        raise LanguageCatalogError(f"question_id_mismatch:{path.name}")
    raw_entries = payload.get("entries")
    if not isinstance(raw_entries, dict):
        raise LanguageCatalogError(f"entries_must_be_mapping:{path.name}")
    entries = [
        _parse_entry(key, value, payload, path.name)
        for key, value in raw_entries.items()
    ]
    return LanguageCatalogFile(
        path=path.name,
        module=str(payload.get("module") or ""),
        question_id=question_id,
        catalog_version=str(payload.get("catalog_version") or ""),
        module_language_version=str(payload.get("module_language_version") or ""),
        schema_version=str(payload.get("schema_version") or ""),
        status=str(payload.get("status") or ""),
        entries=entries,
    )


def _parse_entry(
    language_key: str,
    raw: object,
    file_payload: dict[str, Any],
    filename: str,
) -> LanguageEntry:
    """Build one LanguageEntry. Optional fields default empty."""
    if not isinstance(raw, dict):
        raise LanguageCatalogError(f"entry_must_be_mapping:{language_key}")
    module = str(raw.get("module") or file_payload.get("module") or "")
    question_id = str(raw.get("question_id") or file_payload.get("question_id") or "")
    if language_key != str(language_key):
        raise LanguageCatalogError(f"invalid_language_key:{filename}")
    return LanguageEntry(
        language_key=language_key,
        module=module,
        question_id=question_id,
        semantic_state=str(raw.get("semantic_state") or ""),
        version=str(raw.get("version") or ""),
        status=str(raw.get("status") or ""),
        audience=str(raw.get("audience") or file_payload.get("audience") or "customer"),
        tone=str(raw.get("tone") or "professional_warm"),
        headline=str(raw.get("headline") or ""),
        meaning=str(raw.get("meaning") or ""),
        plain_customer_text=str(raw.get("plain_customer_text") or ""),
        technical_explanation=str(raw.get("technical_explanation") or ""),
        supporting_fact_templates=_parse_templates(raw.get("supporting_fact_templates")),
        limitation_templates=_parse_templates(raw.get("limitation_templates")),
        closing=str(raw.get("closing") or ""),
        variants=_parse_variants(raw.get("variants")),
        forbidden_terms=[str(item) for item in raw.get("forbidden_terms") or []],
        slots=[str(item) for item in raw.get("slots") or []],
    )


def _parse_templates(raw: object) -> list[LanguageFactTemplate]:
    """Parse supporting-fact or limitation templates."""
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise LanguageCatalogError("templates_must_be_list")
    items: list[LanguageFactTemplate] = []
    for row in raw:
        if not isinstance(row, dict):
            raise LanguageCatalogError("template_must_be_mapping")
        items.append(
            LanguageFactTemplate(
                id=str(row.get("id") or ""),
                template=str(row.get("template") or ""),
                status=str(row.get("status") or "placeholder"),
                source_fact=str(row["source_fact"]) if row.get("source_fact") else None,
                slots=[str(item) for item in row.get("slots") or []],
            )
        )
    return items


def _parse_variants(raw: object) -> list[LanguageVariant]:
    """Parse optional wording variants."""
    if raw is None:
        return []
    if not isinstance(raw, list):
        raise LanguageCatalogError("variants_must_be_list")
    items: list[LanguageVariant] = []
    for row in raw:
        if not isinstance(row, dict):
            raise LanguageCatalogError("variant_must_be_mapping")
        items.append(
            LanguageVariant(
                id=str(row.get("id") or ""),
                headline=str(row.get("headline") or ""),
                meaning=str(row.get("meaning") or ""),
                status=str(row.get("status") or "placeholder"),
            )
        )
    return items


def _read_yaml(path: Path) -> object:
    """Read one YAML document."""
    try:
        return yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise LanguageCatalogError(f"yaml_parse_error:{path.name}") from exc
