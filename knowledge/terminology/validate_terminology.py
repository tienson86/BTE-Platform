#!/usr/bin/env python3
"""Validate Knowledge Terminology Foundation catalogs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TERM_ID_RE = re.compile(r"^TERM-[0-9]{6}$")
STATUSES = {"draft", "review", "official", "deprecated", "placeholder", "archived"}
REQUIRED_GLOSSARY = [
    "term_id",
    "canonical_term",
    "chinese",
    "pinyin",
    "english",
    "definition",
    "category",
    "synonyms",
    "related_terms",
    "status",
]


def _load(name: str) -> dict:
    return json.loads((ROOT / name).read_text(encoding="utf-8"))


def main() -> int:
    """Validate glossary, aliases, and abbreviations consistency."""
    glossary = _load("glossary.json")
    aliases = _load("aliases.json")
    abbreviations = _load("abbreviations.json")

    records = glossary.get("records", [])
    alias_records = aliases.get("records", [])
    abbr_records = abbreviations.get("records", [])

    errors: list[str] = []
    warnings: list[str] = []
    seen_ids: dict[str, int] = {}
    seen_terms: dict[str, str] = {}

    for idx, record in enumerate(records):
        if not isinstance(record, dict):
            errors.append(f"glossary.records[{idx}] must be an object")
            continue
        for field in REQUIRED_GLOSSARY:
            if field not in record:
                errors.append(f"glossary.records[{idx}] missing {field}")

        term_id = str(record.get("term_id", ""))
        if not TERM_ID_RE.match(term_id):
            errors.append(f"invalid term_id: {term_id}")
        elif term_id in seen_ids:
            errors.append(f"duplicate term_id {term_id}")
        else:
            seen_ids[term_id] = idx

        canonical = str(record.get("canonical_term", "")).strip()
        key = canonical.lower()
        if not canonical:
            errors.append(f"{term_id}: empty canonical_term")
        elif key in seen_terms:
            errors.append(f"duplicate canonical_term '{canonical}'")
        else:
            seen_terms[key] = term_id

        status = str(record.get("status", "")).lower()
        if status not in STATUSES:
            errors.append(f"{term_id}: invalid status '{status}'")

        for field in ("chinese", "pinyin", "definition"):
            if str(record.get(field, "")) == "TODO_REVIEW":
                warnings.append(f"{term_id}: {field}=TODO_REVIEW")

        related = record.get("related_terms", [])
        if not isinstance(related, list):
            errors.append(f"{term_id}: related_terms must be array")
        else:
            for related_id in related:
                if related_id not in seen_ids and related_id not in {
                    str(r.get("term_id")) for r in records if isinstance(r, dict)
                }:
                    # deferred check after full pass
                    pass

    # related_terms resolve after full ID set known
    for record in records:
        if not isinstance(record, dict):
            continue
        term_id = str(record.get("term_id", ""))
        for related_id in record.get("related_terms", []) or []:
            if related_id not in seen_ids:
                errors.append(f"{term_id}: related_terms unknown {related_id}")

    for idx, record in enumerate(alias_records):
        if not isinstance(record, dict):
            errors.append(f"aliases.records[{idx}] must be an object")
            continue
        for field in ("alias", "canonical_term_id", "canonical_term"):
            if field not in record:
                errors.append(f"aliases.records[{idx}] missing {field}")
        cid = str(record.get("canonical_term_id", ""))
        if cid and cid not in seen_ids:
            errors.append(f"alias '{record.get('alias')}' points to missing {cid}")

    for idx, record in enumerate(abbr_records):
        if not isinstance(record, dict):
            errors.append(f"abbreviations.records[{idx}] must be an object")
            continue
        for field in ("abbreviation", "canonical_term_id", "canonical_term"):
            if field not in record:
                errors.append(f"abbreviations.records[{idx}] missing {field}")
        cid = str(record.get("canonical_term_id", ""))
        if cid and cid not in seen_ids:
            errors.append(
                f"abbreviation '{record.get('abbreviation')}' points to missing {cid}"
            )

    print(f"glossary_records={len(records)}")
    print(f"alias_records={len(alias_records)}")
    print(f"abbreviation_records={len(abbr_records)}")
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
