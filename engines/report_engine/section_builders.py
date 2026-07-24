"""WP6 section builders — structure from ``06_report_templates``, content from Interpretation."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable

from .interpretation_adapter import build_bind_context
from .knowledge_template_loader import KnowledgeTemplateLoader, TemplateModule
from .section import ReportSection, SectionType


@dataclass(slots=True)
class BuiltSection:
    """One rendered report section plus template provenance."""

    section: ReportSection
    template_id: str
    module_id: str
    source: str
    used_label_codes: tuple[str, ...] = field(default_factory=tuple)


# WP6 builder order → KB module_id
WP6_SECTION_SPECS: tuple[tuple[str, str, str], ...] = (
    ("summary", "01_summary", "summary"),
    ("personality", "02_personality", "personality"),
    ("career", "03_career", "career"),
    ("wealth", "04_wealth", "wealth"),
    ("relationship", "05_relationship", "relationship"),
    ("health", "06_health", "health"),
    ("children", "07_children", "children"),
    ("useful_god", "08_useful_god", "useful_god"),
    ("luck_cycle", "09_luck_cycle", "luck_cycle"),
    ("yearly_fortune", "10_yearly_fortune", "yearly_fortune"),
    ("conclusion", "", "conclusion"),  # no KB module — schema/footer labels
)


def _resolve_path(context: dict[str, Any], path: str) -> Any:
    """Resolve dotted path like ``interpretation.summary.body``."""
    current: Any = context
    for part in path.split("."):
        if isinstance(current, dict) and part in current:
            current = current[part]
        else:
            return None
    return current


def _fill_placeholders(text: str, context: dict[str, Any]) -> str:
    """Replace ``{{key}}`` using placeholder sources when present in text."""
    result = text
    # Direct {{section_key}} style from examples
    interpretation = context.get("interpretation") or {}
    report_context = context.get("report_context") or {}
    replacements = {
        "{{subject_name}}": str(report_context.get("subject_name") or ""),
    }
    for name, payload in interpretation.items():
        if isinstance(payload, dict):
            replacements[f"{{{{section_key}}}}"] = str(payload.get("section_key") or name)
            for field_name, value in payload.items():
                if isinstance(value, str):
                    replacements[f"{{{{{name}.{field_name}}}}}"] = value
    for key, value in replacements.items():
        result = result.replace(key, value)
    return result


def _content_for_block(
    block: dict[str, Any],
    context: dict[str, Any],
    module_name: str,
) -> str:
    """Bind block content_ref to Interpretation fields."""
    content_ref = str(block.get("content_ref") or "").strip()
    if content_ref:
        value = _resolve_path(context, content_ref)
        if value is None and content_ref.startswith("interpretation."):
            # Remap module path aliases (e.g. interpretation.luck_cycle → luck_cycle bag)
            parts = content_ref.split(".")
            if len(parts) >= 3:
                alt = ["interpretation", module_name, *parts[2:]]
                value = _resolve_path(context, ".".join(alt))
        if isinstance(value, list):
            return "\n\n".join(str(item) for item in value if str(item).strip())
        if value is not None:
            return _fill_placeholders(str(value), context)

    # Fallback by block_type
    bag = (context.get("interpretation") or {}).get(module_name) or {}
    block_type = str(block.get("block_type") or "")
    if block_type in {"title", "header"}:
        return str(bag.get("title") or bag.get("summary") or "")
    if block_type in {"summary"}:
        return str(bag.get("summary") or bag.get("body") or "")
    if block_type in {"recommendation"}:
        return str(bag.get("recommendation") or "")
    if block_type in {"list"}:
        paragraphs = bag.get("paragraphs") or []
        return "\n".join(f"- {p}" for p in paragraphs)
    return str(bag.get("body") or bag.get("summary") or "")


def render_module_section(
    *,
    builder_name: str,
    module: TemplateModule | None,
    context: dict[str, Any],
    order: int,
    schema: dict[str, Any] | None = None,
) -> BuiltSection:
    """Render one WP6 section from a Knowledge template module."""
    module_name = builder_name
    if module is not None:
        template = module.select_template()
        module_id = module.module_id
        module_name = module.module_name
        title = module.module_title
        source = "template_examples" if template and template.get("_source") == "template_examples" else "template_index"
    else:
        # Conclusion (no KB module): structure from schema; title from shared labels if provided
        schema = schema or {}
        block_types = list(schema.get("block_types") or ["title", "paragraph", "footer"])
        title = "conclusion"
        label_module = (schema or {}).get("_label_module")
        if isinstance(label_module, TemplateModule):
            title = (
                label_module.label_display("footer")
                or label_module.label_display("title")
                or title
            )
        template = {
            "template_id": "schema_conclusion",
            "template_name": "schema_conclusion",
            "module": "template_schema",
            "title": title,
            "sections": [
                {
                    "section_id": "conclusion_body",
                    "section_key": "conclusion",
                    "title": title,
                    "order": 1,
                    "enabled": True,
                    "blocks": ["c1", "c2"],
                }
            ],
            "blocks": [
                {
                    "block_id": "c1",
                    "block_type": "title",
                    "label_ref": "title",
                    "order": 1,
                    "content_ref": "interpretation.conclusion.title",
                    "enabled": True,
                },
                {
                    "block_id": "c2",
                    "block_type": "paragraph",
                    "label_ref": "paragraph",
                    "order": 2,
                    "content_ref": "interpretation.conclusion.body",
                    "enabled": True,
                },
            ],
            "_source": "template_schema",
            "_block_types": block_types,
        }
        module_id = "template_schema"
        source = "template_schema"

    if not template:
        template = {
            "template_id": f"{module_name}_empty",
            "title": title if module else module_name,
            "sections": [],
            "blocks": [
                {
                    "block_id": "body",
                    "block_type": "paragraph",
                    "label_ref": "paragraph",
                    "order": 1,
                    "content_ref": f"interpretation.{module_name}.body",
                    "enabled": True,
                }
            ],
        }
        source = "fallback_empty"

    blocks_by_id = {
        str(block.get("block_id")): block
        for block in (template.get("blocks") or [])
        if isinstance(block, dict)
    }
    used_labels: list[str] = []
    parts: list[str] = []

    section_defs = list(template.get("sections") or [])
    if section_defs:
        section_defs = sorted(
            [s for s in section_defs if s.get("enabled", True)],
            key=lambda s: int(s.get("order", 0) or 0),
        )
        for section_def in section_defs:
            for block_id in section_def.get("blocks") or []:
                block = blocks_by_id.get(str(block_id))
                if not block or not block.get("enabled", True):
                    continue
                label_ref = str(block.get("label_ref") or "")
                if label_ref:
                    used_labels.append(label_ref)
                label_prefix = ""
                if module is not None and label_ref:
                    label_prefix = module.label_display(label_ref)
                text = _content_for_block(block, context, module_name).strip()
                if not text:
                    continue
                if label_prefix and str(block.get("block_type")) in {
                    "title",
                    "header",
                    "important",
                    "warning",
                    "recommendation",
                    "note",
                    "callout",
                }:
                    parts.append(f"{label_prefix}: {text}" if not text.startswith(label_prefix) else text)
                else:
                    parts.append(text)
    else:
        for block in sorted(
            blocks_by_id.values(),
            key=lambda b: int(b.get("order", 0) or 0),
        ):
            if not block.get("enabled", True):
                continue
            text = _content_for_block(block, context, module_name).strip()
            if text:
                parts.append(text)

    content = "\n\n".join(parts).strip()
    section_title = str(template.get("title") or (module.module_title if module else module_name))
    # Prefer metadata module_title over schema-example titles
    if module is not None:
        section_title = module.module_title

    section_type = SectionType.CONCLUSION if builder_name == "conclusion" else SectionType.INTERPRETATION
    report_section = ReportSection(
        id=builder_name,
        title=section_title,
        type=section_type,
        content=content,
        order=order,
        visible=True,
        metadata={
            "builder": builder_name,
            "module_id": module_id,
            "template_id": str(template.get("template_id") or ""),
            "source": source,
        },
        tags=[builder_name, module_id],
    )
    return BuiltSection(
        section=report_section,
        template_id=str(template.get("template_id") or ""),
        module_id=module_id,
        source=source,
        used_label_codes=tuple(dict.fromkeys(used_labels)),
    )


class SectionBuilderRegistry:
    """Build all WP6 sections from templates + Interpretation bind context."""

    def __init__(self, loader: KnowledgeTemplateLoader | None = None) -> None:
        self.loader = loader or KnowledgeTemplateLoader()

    def build_all(self, interpretation: Any) -> list[BuiltSection]:
        """Build every WP6 section in declared order."""
        context = build_bind_context(interpretation)
        schema = self.loader.load_schema()
        built: list[BuiltSection] = []
        schema_with_labels = dict(schema)
        schema_with_labels["_label_module"] = self.loader.get_module("01_summary")
        for order, (builder_name, module_id, _alias) in enumerate(WP6_SECTION_SPECS, start=1):
            module = self.loader.get_module(module_id) if module_id else None
            built.append(
                render_module_section(
                    builder_name=builder_name,
                    module=module,
                    context=context,
                    order=order,
                    schema=schema_with_labels,
                )
            )
        return built

    # Explicit named builders (public WP6 surface)
    def build_summary(self, interpretation: Any) -> BuiltSection:
        return self._one("summary", interpretation)

    def build_personality(self, interpretation: Any) -> BuiltSection:
        return self._one("personality", interpretation)

    def build_career(self, interpretation: Any) -> BuiltSection:
        return self._one("career", interpretation)

    def build_wealth(self, interpretation: Any) -> BuiltSection:
        return self._one("wealth", interpretation)

    def build_relationship(self, interpretation: Any) -> BuiltSection:
        return self._one("relationship", interpretation)

    def build_health(self, interpretation: Any) -> BuiltSection:
        return self._one("health", interpretation)

    def build_children(self, interpretation: Any) -> BuiltSection:
        return self._one("children", interpretation)

    def build_useful_god(self, interpretation: Any) -> BuiltSection:
        return self._one("useful_god", interpretation)

    def build_luck_cycle(self, interpretation: Any) -> BuiltSection:
        return self._one("luck_cycle", interpretation)

    def build_year(self, interpretation: Any) -> BuiltSection:
        return self._one("yearly_fortune", interpretation)

    def build_conclusion(self, interpretation: Any) -> BuiltSection:
        return self._one("conclusion", interpretation)

    def _one(self, builder_name: str, interpretation: Any) -> BuiltSection:
        for order, (name, module_id, _) in enumerate(WP6_SECTION_SPECS, start=1):
            if name != builder_name:
                continue
            context = build_bind_context(interpretation)
            module = self.loader.get_module(module_id) if module_id else None
            schema = dict(self.loader.load_schema())
            schema["_label_module"] = self.loader.get_module("01_summary")
            return render_module_section(
                builder_name=name,
                module=module,
                context=context,
                order=order,
                schema=schema,
            )
        raise KeyError(builder_name)


# Convenience aliases matching WP6 naming
BUILDERS: dict[str, Callable[[SectionBuilderRegistry, Any], BuiltSection]] = {
    "Summary": SectionBuilderRegistry.build_summary,
    "Personality": SectionBuilderRegistry.build_personality,
    "Career": SectionBuilderRegistry.build_career,
    "Wealth": SectionBuilderRegistry.build_wealth,
    "Relationship": SectionBuilderRegistry.build_relationship,
    "Health": SectionBuilderRegistry.build_health,
    "Children": SectionBuilderRegistry.build_children,
    "Useful God": SectionBuilderRegistry.build_useful_god,
    "Luck Cycle": SectionBuilderRegistry.build_luck_cycle,
    "Year": SectionBuilderRegistry.build_year,
    "Conclusion": SectionBuilderRegistry.build_conclusion,
}
