"""Deterministic JSON rule package loader."""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

from engines.rule_engine.exceptions import RuleLoadError
from engines.rule_engine.models import (
    LoadResult,
    RuleRecord,
    ValidationDiagnostic,
    build_rule_record,
)
from engines.rule_engine.validator import RuleValidator

logger = logging.getLogger(__name__)

_RULE_FILE_SUFFIXES = {".json"}
_SKIP_BASENAMES = frozenset(
    {
        "manifest.json",
        "rule_index.json",
        "statistics.json",
        "dependencies.json",
        "test_cases.json",
        "validation_report.json",
    }
)


class RuleLoader:
    """Recursively discover and load JSON rule packages."""

    def __init__(self, validator: RuleValidator | None = None) -> None:
        self._validator = validator or RuleValidator()

    def discover_files(self, root: Path) -> list[Path]:
        """Return rule JSON files in deterministic path order."""
        if not root.exists():
            raise RuleLoadError(f"Rules root does not exist: {root}")
        if not root.is_dir():
            raise RuleLoadError(f"Rules root is not a directory: {root}")

        files: list[Path] = []
        for path in sorted(root.rglob("*"), key=lambda item: item.as_posix().lower()):
            if not path.is_file():
                continue
            if path.suffix.lower() not in _RULE_FILE_SUFFIXES:
                continue
            if path.name.lower() in _SKIP_BASENAMES:
                continue
            # Prefer package payloads that contain a rules array.
            files.append(path)
        return files

    def load(self, root: Path | str) -> tuple[list[RuleRecord], LoadResult]:
        """Load enabled rules from root with validation diagnostics."""
        root_path = Path(root)
        files = self.discover_files(root_path)
        records: list[RuleRecord] = []
        diagnostics: list[ValidationDiagnostic] = []
        seen_ids: set[str] = set()
        skipped_disabled = 0
        invalid = 0
        source_files: list[str] = []

        for path in files:
            relative = path.relative_to(root_path).as_posix()
            try:
                payload = self._read_json(path)
            except RuleLoadError as exc:
                invalid += 1
                diagnostics.append(
                    ValidationDiagnostic(
                        code="unreadable_file",
                        message=str(exc),
                        severity="error",
                        source_path=relative,
                    )
                )
                continue

            rules = self._extract_rules(payload)
            if rules is None:
                # Not a rule package payload; ignore silently for discovery noise.
                continue

            source_files.append(relative)
            for index, raw in enumerate(rules):
                if not isinstance(raw, dict):
                    invalid += 1
                    diagnostics.append(
                        ValidationDiagnostic(
                            code="invalid_rule",
                            message=f"Rule at index {index} is not an object.",
                            severity="error",
                            source_path=relative,
                        )
                    )
                    continue

                item_diagnostics, recoverable = self._validator.validate_raw(
                    raw,
                    source_path=relative,
                    seen_ids=seen_ids,
                )
                diagnostics.extend(item_diagnostics)
                if not recoverable:
                    invalid += 1
                    continue

                record = build_rule_record(raw, source_path=relative)
                if not record.enabled:
                    skipped_disabled += 1
                    continue

                seen_ids.add(record.id)
                records.append(record)

        # Deterministic runtime order by source path then id.
        records.sort(key=lambda item: (item.source_path.lower(), item.id.lower()))
        result = LoadResult(
            loaded=len(records),
            skipped_disabled=skipped_disabled,
            invalid=invalid,
            diagnostics=tuple(diagnostics),
            source_files=tuple(source_files),
        )
        logger.info(
            "rule_loader.done loaded=%s skipped_disabled=%s invalid=%s files=%s",
            result.loaded,
            result.skipped_disabled,
            result.invalid,
            len(result.source_files),
        )
        return records, result

    @staticmethod
    def _read_json(path: Path) -> Any:
        """Read one JSON file."""
        try:
            with path.open("r", encoding="utf-8-sig") as handle:
                return json.load(handle)
        except (OSError, json.JSONDecodeError) as exc:
            raise RuleLoadError(f"Failed to read rule file '{path}': {exc}") from exc

    @staticmethod
    def _extract_rules(payload: Any) -> list[Any] | None:
        """Extract a rules array from a package or bare list."""
        if isinstance(payload, list):
            return payload
        if isinstance(payload, dict):
            rules = payload.get("rules")
            if isinstance(rules, list):
                return rules
        return None
