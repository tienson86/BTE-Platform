"""Load PACK-01 Knowledge Catalog from markdown units."""

from __future__ import annotations

import logging
import re
from pathlib import Path

from engines.interpretation_engine_v2.strength.contracts.models import (
    CatalogLoadError,
    KnowledgeUnit,
)

logger = logging.getLogger(__name__)

_UNIT_HEADING = re.compile(r"^##\s+(IK-STR-[A-Z]+-\d+)\s*$", re.MULTILINE)
_TABLE_ROW = re.compile(r"^\|\s*([^|]+?)\s*\|\s*([^|]*?)\s*\|$")
_BLOCK_CLAIM = re.compile(
    r"\*\*claim\*\*\s*\n\n(.*?)(?=\n\*\*|\n---|\n## |\Z)",
    re.DOTALL,
)
_BLOCK_LIST = re.compile(
    r"\*\*(supporting_points|limitations)\*\*\s*\n\n(.*?)(?=\n\*\*|\n---|\n## |\Z)",
    re.DOTALL,
)


def default_catalog_root() -> Path:
    """Return default PACK-01 catalog path relative to repo root."""
    return Path(__file__).resolve().parents[4] / "knowledge" / "knowledge_catalog" / "PACK_01_STRENGTH" / "catalog"


class KnowledgeCatalogLoader:
    """Parse Knowledge Catalog markdown into KnowledgeUnit objects."""

    def __init__(self, catalog_root: Path | None = None) -> None:
        self._catalog_root = catalog_root or default_catalog_root()

    def load_all(self) -> list[KnowledgeUnit]:
        """Load every unit under catalog/."""
        if not self._catalog_root.is_dir():
            raise CatalogLoadError(f"Catalog root not found: {self._catalog_root}")

        units: list[KnowledgeUnit] = []
        for path in sorted(self._catalog_root.rglob("*.md")):
            units.extend(self.load_file(path))
        logger.info("Loaded %s knowledge units from %s", len(units), self._catalog_root)
        return units

    def load_file(self, path: Path) -> list[KnowledgeUnit]:
        """Parse one catalog markdown file."""
        text = path.read_text(encoding="utf-8")
        return self.parse_markdown(text)

    def parse_markdown(self, text: str) -> list[KnowledgeUnit]:
        """Parse catalog markdown content."""
        headings = list(_UNIT_HEADING.finditer(text))
        units: list[KnowledgeUnit] = []
        for index, match in enumerate(headings):
            knowledge_id = match.group(1)
            start = match.end()
            end = headings[index + 1].start() if index + 1 < len(headings) else len(text)
            block = text[start:end]
            units.append(self._parse_unit_block(knowledge_id, block))
        return units

    def _parse_unit_block(self, knowledge_id: str, block: str) -> KnowledgeUnit:
        fields = self._parse_field_table(block)
        claim = self._parse_claim(block)
        supporting_points, limitations = self._parse_lists(block)
        return KnowledgeUnit(
            knowledge_id=knowledge_id,
            title=fields.get("title", ""),
            pack=fields.get("pack", "PACK_01_STRENGTH"),
            topic=fields.get("topic", ""),
            purpose=fields.get("purpose", ""),
            domain=fields.get("domain", ""),
            strength_class=fields.get("strength_class", ""),
            customer_mode=fields.get("customer_mode", "ALLOWED"),
            validation_mode=fields.get("validation_mode", "ALLOWED"),
            required_facts=self._split_csv(fields.get("required_facts", "")),
            optional_facts=self._split_csv(fields.get("optional_facts", "")),
            forbidden_conditions=self._split_csv(fields.get("forbidden_conditions", "")),
            required_evidence=fields.get("required_evidence", "FULL"),
            customer_value=fields.get("customer_value", "MEDIUM"),
            specificity=fields.get("specificity", "GENERIC"),
            priority=fields.get("priority", "NORMAL"),
            duplicate_cluster=fields.get("duplicate_cluster", "NONE"),
            conflicts_with=self._split_csv(fields.get("conflicts_with", "")),
            reason_codes=self._split_csv(fields.get("reason_codes", "")),
            narrative_weight=fields.get("narrative_weight", "SUPPORTING"),
            version=fields.get("version", "1.0.0"),
            status=fields.get("status", "Draft"),
            source_document=fields.get("source_document", ""),
            claim=claim.strip(),
            supporting_points=supporting_points,
            limitations=limitations,
        )

    @staticmethod
    def _parse_field_table(block: str) -> dict[str, str]:
        fields: dict[str, str] = {}
        for line in block.splitlines():
            row = _TABLE_ROW.match(line.strip())
            if not row:
                continue
            key = row.group(1).strip()
            value = row.group(2).strip()
            if key.lower() in {"field", "---"}:
                continue
            fields[key] = value
        return fields

    @staticmethod
    def _parse_claim(block: str) -> str:
        match = _BLOCK_CLAIM.search(block)
        if not match:
            return ""
        return match.group(1).strip()

    @staticmethod
    def _parse_lists(block: str) -> tuple[list[str], list[str]]:
        supporting: list[str] = []
        limitations: list[str] = []
        for match in _BLOCK_LIST.finditer(block):
            name = match.group(1)
            body = match.group(2).strip()
            items = KnowledgeCatalogLoader._bullet_items(body)
            if name == "supporting_points":
                supporting = items
            else:
                limitations = items
        return supporting, limitations

    @staticmethod
    def _bullet_items(body: str) -> list[str]:
        if not body or body.startswith("(empty"):
            return []
        items: list[str] = []
        for line in body.splitlines():
            line = line.strip()
            if line.startswith("- "):
                items.append(line[2:].strip())
            elif line:
                items.append(line)
        return items

    @staticmethod
    def _split_csv(value: str) -> list[str]:
        if not value:
            return []
        return [part.strip() for part in value.split(",") if part.strip()]
