"""
Knowledge Rule Loader (WP4)

Load interpretation Knowledge Base JSON into matchable rule dicts.

Preserves ``conditions`` / ``required_conditions`` for Rule Adapter.
Does not invent BaZi logic.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)

# Folder → WP4 section key
FOLDER_SECTION_MAP: dict[str, str] = {
    "01_strength_rules": "strength",
    "02_season_rules": "summary",
    "03_temperature_rules": "warning",
    "04_pattern_rules": "pattern",
    "05_special_case_rules": "warning",
    "06_follow_pattern_rules": "pattern",
    "07_combination_rules": "warning",
    "08_priority_rules": "summary",
}

CATEGORY_SECTION_MAP: dict[str, str] = {
    "standard_pattern": "pattern",
    "special_pattern": "pattern",
    "follow_pattern": "pattern",
    "strength": "strength",
    "season": "summary",
    "temperature": "warning",
    "combination": "warning",
    "career": "career",
    "wealth": "wealth",
    "relationship": "relationship",
    "health": "health",
    "useful_god": "useful_god",
}


def default_knowledge_root() -> Path:
    """Default path to ``05_rule_database`` under interpretation knowledge."""
    return (
        Path(__file__).resolve().parent
        / "knowledge"
        / "05_rule_database"
    )


def load_multi_json(path: Path) -> list[Any]:
    """Decode one or more concatenated JSON documents."""
    text = path.read_text(encoding="utf-8")
    decoder = json.JSONDecoder()
    idx = 0
    docs: list[Any] = []
    while idx < len(text):
        while idx < len(text) and text[idx].isspace():
            idx += 1
        if idx >= len(text):
            break
        try:
            obj, end = decoder.raw_decode(text, idx)
        except json.JSONDecodeError:
            break
        docs.append(obj)
        idx = end
    return docs


class KnowledgeRuleLoader:
    """Walk Knowledge Base folders and normalize rules for Adapter matching."""

    def __init__(self, root: str | Path | None = None) -> None:
        self.root = Path(root) if root else default_knowledge_root()

    def load(self) -> list[dict[str, Any]]:
        """Load all enabled rules from the knowledge tree."""
        if not self.root.exists():
            logger.warning("Knowledge rule root not found: %s", self.root)
            return []

        rules: list[dict[str, Any]] = []
        for path in sorted(self.root.rglob("*.json")):
            if path.name.lower().startswith("readme"):
                continue
            # Skip label/example-only indexes that are not matchable rules
            if path.name.endswith(("_labels.json", "_examples.json", "_index.json")):
                continue
            if path.name in {"metadata.json", "sentence_schema.json"}:
                continue
            try:
                docs = load_multi_json(path)
            except OSError as exc:
                logger.warning("Skip %s: %s", path, exc)
                continue
            folder = path.parent.name
            for doc in docs:
                for item in self._iter_items(doc):
                    if not isinstance(item, dict):
                        continue
                    if item.get("enabled") is False:
                        continue
                    # Need something matchable
                    has_condition_payload = any(
                        key in item
                        and item.get(key) not in (None, "", {}, [])
                        for key in (
                            "conditions",
                            "condition",
                            "required_conditions",
                        )
                    )
                    # Explicit empty conditions list = unconditional
                    explicit_empty = item.get("conditions") == []
                    if not has_condition_payload and not explicit_empty:
                        continue
                    normalized = self._normalize(item, folder=folder, source=str(path))
                    if normalized:
                        rules.append(normalized)
        return rules

    @staticmethod
    def _iter_items(doc: Any) -> list[Any]:
        if isinstance(doc, list):
            return doc
        if isinstance(doc, dict):
            for key in ("rules", "conditions", "items", "data"):
                value = doc.get(key)
                if isinstance(value, list):
                    return value
            # Single rule object
            if "id" in doc or "rule_id" in doc:
                return [doc]
        return []

    def _normalize(
        self,
        item: dict[str, Any],
        *,
        folder: str,
        source: str,
    ) -> dict[str, Any] | None:
        rule_id = str(
            item.get("id")
            or item.get("rule_id")
            or item.get("condition_id")
            or item.get("pattern_code")
            or ""
        ).strip()
        if not rule_id:
            return None

        category = str(item.get("category") or item.get("rule_type") or folder)
        section = self._resolve_section(item, folder, category)
        priority = self._number(item.get("priority"), default=50)
        score = self._number(item.get("score"), default=float(priority))
        confidence = self._number(
            item.get("confidence"),
            default=min(1.0, max(0.0, float(priority) / 100.0)),
        )

        description = str(
            item.get("description")
            or item.get("pattern_name")
            or item.get("condition_name")
            or item.get("rule_name")
            or rule_id
        )

        polarity = str(item.get("polarity") or "neutral").strip().lower()
        if polarity not in {"positive", "negative", "neutral", "warning"}:
            polarity = self._infer_polarity(folder, category, item)

        rule: dict[str, Any] = {
            "rule_id": rule_id,
            "rule_name": str(
                item.get("rule_name")
                or item.get("pattern_name")
                or item.get("condition_name")
                or rule_id
            ),
            "category": category,
            "layer": str(item.get("layer") or folder),
            "section": section,
            "description": description,
            "polarity": polarity,
            "priority": int(priority) if float(priority).is_integer() else priority,
            "score": score,
            "confidence": confidence,
            "tags": list(item.get("tags") or []),
            "source": source,
            "result": item.get("result"),
        }

        # Preserve Adapter-friendly condition shapes
        if "conditions" in item:
            rule["conditions"] = item["conditions"]
        if "required_conditions" in item:
            rule["required_conditions"] = item["required_conditions"]
            rule["match_type"] = item.get("match_type", "all")
        if "condition" in item:
            rule["condition"] = item["condition"]

        return rule

    def _resolve_section(
        self,
        item: dict[str, Any],
        folder: str,
        category: str,
    ) -> str:
        explicit = item.get("section")
        if explicit:
            return str(explicit).strip()
        if category in CATEGORY_SECTION_MAP:
            return CATEGORY_SECTION_MAP[category]
        if folder in FOLDER_SECTION_MAP:
            return FOLDER_SECTION_MAP[folder]
        return "summary"

    @staticmethod
    def _infer_polarity(folder: str, category: str, item: dict[str, Any]) -> str:
        text = f"{folder} {category} {item.get('description', '')}".lower()
        if any(token in text for token in ("weak", "nhuoc", "destroy", "clash", "harm")):
            return "negative"
        if any(token in text for token in ("warning", "conflict", "risk")):
            return "warning"
        if any(token in text for token in ("strong", "vuong", "success", "support")):
            return "positive"
        return "neutral"

    @staticmethod
    def _number(value: Any, default: float = 0.0) -> float:
        if value in ("", None):
            return default
        try:
            return float(value)
        except (TypeError, ValueError):
            return default
