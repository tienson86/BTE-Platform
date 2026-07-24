"""Template coverage reporting for WP6 Report Engine."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterable

from .knowledge_template_loader import KnowledgeTemplateLoader
from .section_builders import BuiltSection, WP6_SECTION_SPECS


@dataclass(slots=True)
class TemplateCoverageReport:
    """Used / unused template assets and coverage ratio."""

    templates_used: list[dict[str, Any]] = field(default_factory=list)
    templates_unused: list[dict[str, Any]] = field(default_factory=list)
    modules_covered: list[str] = field(default_factory=list)
    modules_missing: list[str] = field(default_factory=list)
    coverage_ratio: float = 0.0
    notes: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Serialize coverage report."""
        return {
            "templates_used": self.templates_used,
            "templates_unused": self.templates_unused,
            "modules_covered": self.modules_covered,
            "modules_missing": self.modules_missing,
            "coverage_ratio": self.coverage_ratio,
            "used_count": len(self.templates_used),
            "unused_count": len(self.templates_unused),
            "notes": self.notes,
        }

    def to_markdown(self) -> str:
        """Human-readable coverage markdown."""
        lines = [
            "# WP6 Template Coverage",
            "",
            f"- Coverage: **{self.coverage_ratio:.2%}**",
            f"- Used: **{len(self.templates_used)}**",
            f"- Unused: **{len(self.templates_unused)}**",
            "",
            "## Templates Used",
            "",
        ]
        for item in self.templates_used:
            lines.append(
                f"- `{item.get('template_id')}` ({item.get('module_id')}, {item.get('source')})"
            )
        lines.extend(["", "## Templates Unused", ""])
        if not self.templates_unused:
            lines.append("- (none)")
        for item in self.templates_unused:
            lines.append(
                f"- `{item.get('template_id')}` ({item.get('module_id')}, {item.get('source')})"
            )
        if self.notes:
            lines.extend(["", "## Notes", ""])
            for note in self.notes:
                lines.append(f"- {note}")
        lines.append("")
        return "\n".join(lines)


class TemplateCoverageAnalyzer:
    """Compare KB inventory against sections actually rendered."""

    def __init__(self, loader: KnowledgeTemplateLoader | None = None) -> None:
        self.loader = loader or KnowledgeTemplateLoader()

    def analyze(self, built_sections: Iterable[BuiltSection]) -> TemplateCoverageReport:
        """Compute used vs unused template assets."""
        inventory = self.loader.inventory()
        assets = list(inventory.get("assets") or [])
        built = list(built_sections)

        used_keys: set[tuple[str, str]] = set()
        used_rows: list[dict[str, Any]] = []
        modules_covered: list[str] = []

        for item in built:
            key = (item.module_id, item.template_id)
            if key not in used_keys and item.template_id:
                used_keys.add(key)
                used_rows.append(
                    {
                        "module_id": item.module_id,
                        "template_id": item.template_id,
                        "source": item.source,
                        "builder": item.section.id,
                    }
                )
            if item.module_id and item.module_id not in modules_covered:
                modules_covered.append(item.module_id)

        unused_rows: list[dict[str, Any]] = []
        for asset in assets:
            key = (str(asset.get("module_id")), str(asset.get("template_id")))
            if key in used_keys:
                continue
            # Example layout used when index empty counts as used via built source
            if asset.get("source") == "template_examples":
                module_id = str(asset.get("module_id"))
                if any(
                    row.get("module_id") == module_id and row.get("source") == "template_examples"
                    for row in used_rows
                ):
                    # Same module example selected — mark matching template_id used
                    if any(
                        row.get("template_id") == asset.get("template_id") for row in used_rows
                    ):
                        continue
            unused_rows.append(dict(asset))

        # Refine: if module used an example, mark that example template_id used only
        selected_example_ids = {
            (row["module_id"], row["template_id"])
            for row in used_rows
            if row.get("source") == "template_examples"
        }
        unused_rows = [
            row
            for row in unused_rows
            if (str(row.get("module_id")), str(row.get("template_id")))
            not in selected_example_ids
        ]

        module_ids = list(inventory.get("module_ids") or [])
        required_modules = [module_id for _, module_id, _ in WP6_SECTION_SPECS if module_id]
        modules_missing = [m for m in required_modules if m not in modules_covered]

        total = len(used_rows) + len(unused_rows)
        ratio = (len(used_rows) / total) if total else 1.0

        notes: list[str] = []
        if any(row.module_id == "template_schema" for row in built):
            notes.append(
                "Conclusion has no KB module; rendered via template_schema.json structure."
            )
        empty_index = [
            m
            for m in module_ids
            if not (self.loader.get_module(m).index_entries if self.loader.get_module(m) else [])
        ]
        if empty_index:
            notes.append(
                "V1 template_index is empty for: " + ", ".join(empty_index) + "; using examples."
            )

        return TemplateCoverageReport(
            templates_used=used_rows,
            templates_unused=unused_rows,
            modules_covered=modules_covered,
            modules_missing=modules_missing,
            coverage_ratio=round(ratio, 4),
            notes=notes,
        )

    def write_report(
        self,
        report: TemplateCoverageReport,
        output_dir: str | Path,
    ) -> dict[str, Path]:
        """Write JSON + Markdown coverage files."""
        output = Path(output_dir)
        output.mkdir(parents=True, exist_ok=True)
        json_path = output / "wp6_template_coverage.json"
        md_path = output / "wp6_template_coverage.md"
        json_path.write_text(
            json.dumps(report.to_dict(), ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        md_path.write_text(report.to_markdown(), encoding="utf-8")
        return {"json": json_path, "markdown": md_path}
