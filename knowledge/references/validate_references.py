#!/usr/bin/env python3
"""Validate Knowledge Reference Library catalogs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
REF_ID_RE = re.compile(r"^REF-[0-9]{6}$")
CATEGORIES = {"classic", "modern", "paper", "internal"}
SOURCE_TYPES = {
    "classical_text",
    "commentary",
    "modern_book",
    "journal_article",
    "internal_document",
}
STATUSES = {"draft", "review", "official", "deprecated", "placeholder"}
REQUIRED_FIELDS = [
    "reference_id",
    "title_original",
    "title_english",
    "author",
    "dynasty",
    "estimated_year",
    "category",
    "school",
    "language",
    "source_type",
    "canonical_status",
    "description",
    "citation_format",
    "identifier",
    "publisher",
    "edition",
    "volume",
    "chapter_support",
    "notes",
    "keywords",
    "related_modules",
]


def main() -> int:
    """Run validation and print a machine-readable summary."""
    refs_path = ROOT / "references.json"
    index_path = ROOT / "reference_index.json"
    refs_doc = json.loads(refs_path.read_text(encoding="utf-8"))
    index_doc = json.loads(index_path.read_text(encoding="utf-8"))
    records = refs_doc.get("records", [])
    entries = index_doc.get("entries", [])

    errors: list[str] = []
    warnings: list[str] = []

    if not isinstance(records, list):
        errors.append("references.json records must be a list")
        records = []
    if not isinstance(entries, list):
        errors.append("reference_index.json entries must be a list")
        entries = []

    seen_ids: dict[str, int] = {}
    seen_titles: dict[str, str] = {}

    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"records[{idx}] must be an object")
            continue
        for field in REQUIRED_FIELDS:
            if field not in record:
                errors.append(f"records[{idx}] missing required field: {field}")

        ref_id = str(record.get("reference_id", ""))
        if not REF_ID_RE.match(ref_id):
            errors.append(f"records[{idx}] invalid reference_id: {ref_id}")
        elif ref_id in seen_ids:
            errors.append(
                f"duplicate reference_id {ref_id} "
                f"(records[{seen_ids[ref_id]}] and records[{idx}])"
            )
        else:
            seen_ids[ref_id] = idx

        title = str(record.get("title_english", "")).strip()
        title_key = title.lower()
        if not title:
            errors.append(f"records[{idx}] empty title_english")
        elif title_key in seen_titles:
            errors.append(
                f"duplicate title_english '{title}' "
                f"({seen_titles[title_key]} and {ref_id})"
            )
        else:
            seen_titles[title_key] = ref_id

        if not str(record.get("title_original", "")).strip():
            errors.append(f"{ref_id}: empty title_original")

        category = str(record.get("category", ""))
        if category not in CATEGORIES:
            errors.append(f"{ref_id}: invalid category '{category}'")

        source_type = str(record.get("source_type", ""))
        if source_type not in SOURCE_TYPES:
            errors.append(f"{ref_id}: invalid source_type '{source_type}'")

        status = str(record.get("canonical_status", ""))
        if status not in STATUSES:
            errors.append(f"{ref_id}: invalid canonical_status '{status}'")

        for list_field in ("chapter_support", "keywords", "related_modules"):
            if list_field in record and not isinstance(record[list_field], list):
                errors.append(f"{ref_id}: {list_field} must be an array")

        for field in (
            "author",
            "dynasty",
            "estimated_year",
            "identifier",
            "publisher",
            "edition",
            "volume",
        ):
            if str(record.get(field, "")) == "TODO_REVIEW":
                warnings.append(f"{ref_id}: {field}=TODO_REVIEW")

    index_ids = set()
    for idx, entry in enumerate(entries):
        if not isinstance(entry, dict):
            errors.append(f"entries[{idx}] must be an object")
            continue
        for field in (
            "reference_id",
            "title",
            "category",
            "keywords",
            "related_modules",
        ):
            if field not in entry:
                errors.append(f"entries[{idx}] missing field: {field}")
        ref_id = str(entry.get("reference_id", ""))
        index_ids.add(ref_id)
        if ref_id and ref_id not in seen_ids:
            errors.append(f"index entry {ref_id} missing from references.json")

    for ref_id in sorted(seen_ids):
        if ref_id not in index_ids:
            errors.append(f"record {ref_id} missing from reference_index.json")

    print(f"records_checked={len(records)}")
    print(f"index_entries={len(entries)}")
    print(f"error_count={len(errors)}")
    print(f"warning_count={len(warnings)}")
    for item in errors:
        print(f"ERROR\t{item}")
    for item in warnings:
        print(f"WARNING\t{item}")
    print(f"ok={len(errors) == 0}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
