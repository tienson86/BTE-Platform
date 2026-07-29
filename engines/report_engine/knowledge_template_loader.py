"""Load report templates from Knowledge Base ``06_report_templates``.

Read-only. Does not mutate the Knowledge Base.
"""

from __future__ import annotations

import json
import logging
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


def default_templates_root() -> Path:
    """Resolve ``knowledge/06_report_templates`` relative to this package."""
    return (
        Path(__file__).resolve().parents[1]
        / "interpretation_engine"
        / "knowledge"
        / "06_report_templates"
    )


@dataclass(slots=True)
class TemplateModule:
    """One module folder under ``06_report_templates``."""

    module_id: str
    module_name: str
    module_title: str
    path: Path
    metadata: dict[str, Any] = field(default_factory=dict)
    index: dict[str, Any] = field(default_factory=dict)
    labels: dict[str, Any] = field(default_factory=dict)
    examples: dict[str, Any] = field(default_factory=dict)

    @property
    def index_entries(self) -> list[dict[str, Any]]:
        """Indexed template entries (may be empty in V1)."""
        return list(self.index.get("templates") or [])

    @property
    def example_templates(self) -> list[dict[str, Any]]:
        """Schema example templates used as layout when index is empty."""
        templates: list[dict[str, Any]] = []
        for item in self.examples.get("examples") or []:
            template = item.get("template")
            if isinstance(template, dict):
                templates.append(template)
        return templates

    def label_display(self, label_code: str, default: str = "") -> str:
        """Resolve display_name for a label_code."""
        for label in self.labels.get("labels") or []:
            if str(label.get("label_code")) == label_code:
                return str(label.get("display_name") or label.get("label_name") or default)
        return default

    def select_template(self) -> dict[str, Any] | None:
        """
        Select the highest-priority enabled template.

        V1: index is empty → fall back to schema example layout (structure only).
        """
        entries = [e for e in self.index_entries if e.get("enabled", True)]
        if entries:
            entries.sort(key=lambda e: int(e.get("priority", 0) or 0), reverse=True)
            entry = entries[0]
            file_ref = entry.get("file_ref")
            if file_ref:
                path = self.path / str(file_ref)
                if path.exists():
                    return json.loads(path.read_text(encoding="utf-8"))
            # Entry without file — synthesize minimal template from entry + labels
            return {
                "template_id": entry.get("template_id"),
                "template_name": entry.get("template_name"),
                "module": self.module_id,
                "title": self.module_title,
                "priority": entry.get("priority", 50),
                "sections": [
                    {
                        "section_id": f"{self.module_name}_body",
                        "section_key": "body",
                        "title": self.label_display("paragraph", "Body"),
                        "order": 1,
                        "enabled": True,
                        "blocks": ["body"],
                    }
                ],
                "blocks": [
                    {
                        "block_id": "body",
                        "block_type": "paragraph",
                        "label_ref": "paragraph",
                        "order": 1,
                        "content_ref": f"interpretation.{self.module_name}.body",
                        "enabled": True,
                    }
                ],
                "enabled": True,
            }

        examples = self.example_templates
        if not examples:
            return None
        # Prefer highest priority example; allow disabled examples as structure-only
        ranked = sorted(
            examples,
            key=lambda t: int(t.get("priority", 0) or 0),
            reverse=True,
        )
        template = dict(ranked[0])
        template["title"] = self.module_title or template.get("title", self.module_name)
        # Strip schema-example decoration from title
        title = str(template.get("title") or self.module_title)
        template["title"] = title.replace("[SCHEMA EXAMPLE]", "").strip() or self.module_title
        template["enabled"] = True
        template["_source"] = "template_examples"
        return template


class KnowledgeTemplateLoader:
    """Read-only loader for ``06_report_templates``."""

    def __init__(self, templates_root: str | Path | None = None) -> None:
        self.root = Path(templates_root) if templates_root else default_templates_root()
        self._modules: dict[str, TemplateModule] | None = None
        self._schema: dict[str, Any] | None = None

    def load_schema(self) -> dict[str, Any]:
        """Load shared ``template_schema.json``."""
        if self._schema is not None:
            return self._schema
        path = self.root / "template_schema.json"
        self._schema = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
        return self._schema

    def load_modules(self) -> dict[str, TemplateModule]:
        """Load all module folders."""
        if self._modules is not None:
            return self._modules

        modules: dict[str, TemplateModule] = {}
        if not self.root.exists():
            logger.warning("Report templates root missing: %s", self.root)
            self._modules = modules
            return modules

        for path in sorted(self.root.iterdir()):
            if not path.is_dir():
                continue
            metadata_path = path / "metadata.json"
            if not metadata_path.exists():
                continue
            metadata = self._read_json(metadata_path)
            module_id = str(metadata.get("module_id") or path.name)
            module = TemplateModule(
                module_id=module_id,
                module_name=str(metadata.get("module_name") or path.name),
                module_title=str(metadata.get("module_title") or metadata.get("module_name") or path.name),
                path=path,
                metadata=metadata,
                index=self._read_json(path / "template_index.json"),
                labels=self._read_json(path / "template_labels.json"),
                examples=self._read_json(path / "template_examples.json"),
            )
            modules[module_id] = module
            modules[module.module_name] = module

        self._modules = modules
        return modules

    def get_module(self, module_id_or_name: str) -> TemplateModule | None:
        """Lookup module by id (``01_summary``) or name (``summary``)."""
        return self.load_modules().get(module_id_or_name)

    def list_module_ids(self) -> list[str]:
        """Return canonical module ids from schema or disk."""
        schema = self.load_schema()
        ids = list(schema.get("module_ids") or [])
        if ids:
            return ids
        return sorted(
            {
                m.module_id
                for m in self.load_modules().values()
                if m.module_id.startswith(("0", "1"))
            }
        )

    def inventory(self) -> dict[str, Any]:
        """Inventory of template assets for coverage reporting."""
        used_candidates: list[dict[str, Any]] = []
        for module_id in self.list_module_ids():
            module = self.get_module(module_id)
            if module is None:
                continue
            for entry in module.index_entries:
                used_candidates.append(
                    {
                        "module_id": module_id,
                        "template_id": entry.get("template_id"),
                        "source": "template_index",
                        "enabled": bool(entry.get("enabled", True)),
                    }
                )
            for template in module.example_templates:
                used_candidates.append(
                    {
                        "module_id": module_id,
                        "template_id": template.get("template_id"),
                        "source": "template_examples",
                        "enabled": bool(template.get("enabled", False)),
                    }
                )
        return {
            "root": str(self.root),
            "module_ids": self.list_module_ids(),
            "assets": used_candidates,
            "schema_id": self.load_schema().get("schema_id"),
        }

    @staticmethod
    def _read_json(path: Path) -> dict[str, Any]:
        if not path.exists():
            return {}
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            logger.warning("Failed to read %s: %s", path, exc)
            return {}
        return data if isinstance(data, dict) else {}
