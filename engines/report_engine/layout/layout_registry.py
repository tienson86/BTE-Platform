"""Deterministic RE-2 layout stage registry."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence

from engines.report_engine.layout.layout_context import LAYOUT_VERSION, LayoutError

STAGE_DOCUMENT = "document_builder"
STAGE_SECTION = "section_builder"
STAGE_BLOCK = "block_builder"
STAGE_THEME = "theme_resolver"
STAGE_LAYOUT = "layout_resolver"
STAGE_ASSET = "asset_resolver"
STAGE_TOC = "toc_builder"
STAGE_ASSEMBLY = "assembly"

CANONICAL_STAGE_ORDER: tuple[str, ...] = (
    STAGE_DOCUMENT,
    STAGE_SECTION,
    STAGE_BLOCK,
    STAGE_THEME,
    STAGE_LAYOUT,
    STAGE_ASSET,
    STAGE_TOC,
    STAGE_ASSEMBLY,
)


@dataclass(frozen=True, slots=True)
class LayoutStageRecord:
    """Immutable catalog entry for one layout stage."""

    stage_id: str
    component: str
    version: str
    dependencies: tuple[str, ...]
    consumed_inputs: tuple[str, ...]
    published_outputs: tuple[str, ...]
    enabled: bool
    deterministic: bool

    def to_dict(self) -> dict[str, object]:
        """Serialize the stage catalog record."""
        return {
            "stage_id": self.stage_id,
            "component": self.component,
            "version": self.version,
            "dependencies": list(self.dependencies),
            "consumed_inputs": list(self.consumed_inputs),
            "published_outputs": list(self.published_outputs),
            "enabled": self.enabled,
            "deterministic": self.deterministic,
        }


def _record(
    stage_id: str,
    *,
    dependencies: tuple[str, ...],
    consumed_inputs: tuple[str, ...],
    published_outputs: tuple[str, ...],
) -> LayoutStageRecord:
    return LayoutStageRecord(
        stage_id=stage_id,
        component=stage_id,
        version=LAYOUT_VERSION,
        dependencies=dependencies,
        consumed_inputs=consumed_inputs,
        published_outputs=published_outputs,
        enabled=True,
        deterministic=True,
    )


def _default_records() -> tuple[LayoutStageRecord, ...]:
    upstream = ("report_context", "canonical_interpretation_result")
    return (
        _record(STAGE_DOCUMENT, dependencies=(), consumed_inputs=upstream, published_outputs=("document",)),
        _record(
            STAGE_SECTION,
            dependencies=(STAGE_DOCUMENT,),
            consumed_inputs=upstream + ("document",),
            published_outputs=("sections",),
        ),
        _record(
            STAGE_BLOCK,
            dependencies=(STAGE_SECTION,),
            consumed_inputs=("sections",),
            published_outputs=("blocks",),
        ),
        _record(
            STAGE_THEME,
            dependencies=(STAGE_DOCUMENT,),
            consumed_inputs=upstream,
            published_outputs=("theme",),
        ),
        _record(
            STAGE_LAYOUT,
            dependencies=(STAGE_DOCUMENT, STAGE_SECTION, STAGE_BLOCK),
            consumed_inputs=("document", "sections", "blocks"),
            published_outputs=("layout",),
        ),
        _record(
            STAGE_ASSET,
            dependencies=(STAGE_BLOCK,),
            consumed_inputs=upstream + ("blocks",),
            published_outputs=("assets",),
        ),
        _record(
            STAGE_TOC,
            dependencies=(STAGE_SECTION,),
            consumed_inputs=("sections",),
            published_outputs=("toc",),
        ),
        _record(
            STAGE_ASSEMBLY,
            dependencies=(
                STAGE_DOCUMENT,
                STAGE_SECTION,
                STAGE_BLOCK,
                STAGE_THEME,
                STAGE_LAYOUT,
                STAGE_ASSET,
                STAGE_TOC,
            ),
            consumed_inputs=("document", "sections", "blocks", "theme", "layout", "assets", "toc"),
            published_outputs=("canonical_report_layout",),
        ),
    )


class LayoutRegistry:
    """Read-only catalog of RE-2 layout stages."""

    def __init__(self, records: Iterable[LayoutStageRecord] | None = None) -> None:
        """Load default or injected stage records."""
        catalog = tuple(records) if records is not None else _default_records()
        ids = [item.stage_id for item in catalog]
        if len(ids) != len(set(ids)):
            raise LayoutError("duplicate_stage_id")
        by_id = {item.stage_id: item for item in catalog}
        ordered = tuple(by_id[stage_id] for stage_id in CANONICAL_STAGE_ORDER if stage_id in by_id)
        extra = tuple(item for item in catalog if item.stage_id not in CANONICAL_STAGE_ORDER)
        self._records = ordered + extra
        self._by_id = {item.stage_id: item for item in self._records}

    @classmethod
    def default(cls) -> LayoutRegistry:
        """Return the frozen default layout catalog."""
        return cls()

    def get(self, stage_id: str) -> LayoutStageRecord:
        """Return one stage record or raise."""
        try:
            return self._by_id[stage_id]
        except KeyError as exc:
            raise LayoutError(f"unknown_stage:{stage_id}") from exc

    def registered_ids(self) -> tuple[str, ...]:
        """Return stage identifiers in canonical order."""
        return tuple(item.stage_id for item in self._records)

    def resolve_order(self, requested: Sequence[str] | None = None) -> tuple[str, ...]:
        """Return requested stages in dependency order."""
        requested_ids = tuple(requested) if requested is not None else self.registered_ids()
        requested_set = set(requested_ids)
        unknown = requested_set - set(self._by_id)
        if unknown:
            raise LayoutError(f"unknown_stages:{','.join(sorted(unknown))}")
        ordered: list[str] = []
        for stage_id in CANONICAL_STAGE_ORDER:
            if stage_id not in requested_set:
                continue
            record = self.get(stage_id)
            missing = [dep for dep in record.dependencies if dep not in requested_set]
            if missing:
                raise LayoutError(f"missing_dependencies:{stage_id}:{','.join(missing)}")
            if any(dep not in ordered for dep in record.dependencies):
                raise LayoutError(f"dependency_order:{stage_id}")
            ordered.append(stage_id)
        return tuple(ordered)

    def to_list(self) -> list[dict[str, object]]:
        """Serialize the full layout registry."""
        return [item.to_dict() for item in self._records]
