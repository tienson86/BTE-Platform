"""Canonical render model. Presentation identities only. No business logic."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence

from engines.report_engine.rendering.rendering_context import RenderingContext


@dataclass(slots=True)
class RenderPage:
    """Logical render page derived from layout page hierarchy."""

    page_id: str
    sequence: int
    section_id: str
    block_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize one render page."""
        return {
            "page_id": self.page_id,
            "sequence": self.sequence,
            "section_id": self.section_id,
            "block_ids": list(self.block_ids),
        }


@dataclass(slots=True)
class RenderBlock:
    """Logical render block. Type and source refs only."""

    block_id: str
    section_id: str
    block_type: str
    source_refs: tuple[str, ...]
    asset_ids: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize one render block."""
        return {
            "block_id": self.block_id,
            "section_id": self.section_id,
            "block_type": self.block_type,
            "source_refs": list(self.source_refs),
            "asset_ids": list(self.asset_ids),
        }


@dataclass(slots=True)
class RenderAssetRef:
    """Embedded asset reference. No binary payload."""

    asset_id: str
    asset_kind: str
    source_ref: str
    embed_ref: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize one asset reference."""
        return {
            "asset_id": self.asset_id,
            "asset_kind": self.asset_kind,
            "source_ref": self.source_ref,
            "embed_ref": self.embed_ref,
        }


@dataclass(slots=True)
class RenderStyle:
    """Theme identifier set. Not CSS."""

    theme_id: str
    palette_id: str
    spacing_id: str
    typography_id: str
    icon_set_id: str

    def to_dict(self) -> dict[str, Any]:
        """Serialize style identifiers."""
        return {
            "theme_id": self.theme_id,
            "palette_id": self.palette_id,
            "spacing_id": self.spacing_id,
            "typography_id": self.typography_id,
            "icon_set_id": self.icon_set_id,
        }


@dataclass(slots=True)
class RenderModel:
    """Canonical in-memory render model consumed by format renderers."""

    document_id: str
    pages: tuple[RenderPage, ...]
    blocks: tuple[RenderBlock, ...]
    assets: tuple[RenderAssetRef, ...]
    styles: RenderStyle
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize the render model."""
        return {
            "document_id": self.document_id,
            "pages": [item.to_dict() for item in self.pages],
            "blocks": [item.to_dict() for item in self.blocks],
            "assets": [item.to_dict() for item in self.assets],
            "styles": self.styles.to_dict(),
            "metadata": dict(self.metadata),
        }


@dataclass(slots=True)
class RenderArtifact:
    """In-memory renderer output. No filesystem path."""

    artifact_id: str
    renderer: str
    mime_type: str
    content: str
    metadata: dict[str, Any]
    assets: tuple[dict[str, Any], ...]

    def to_dict(self) -> dict[str, Any]:
        """Serialize the render artifact."""
        return {
            "artifact_id": self.artifact_id,
            "renderer": self.renderer,
            "mime_type": self.mime_type,
            "content": self.content,
            "metadata": dict(self.metadata),
            "assets": [dict(item) for item in self.assets],
        }


def build_render_model(
    context: RenderingContext,
    *,
    assets: Sequence[RenderAssetRef] | None = None,
) -> RenderModel:
    """Project a sealed layout snapshot into the canonical render model."""
    layout = context.layout_snapshot()
    document = layout.get("document") if isinstance(layout.get("document"), Mapping) else {}
    theme = layout.get("theme") if isinstance(layout.get("theme"), Mapping) else {}
    blocks_in = [item for item in layout.get("blocks") or () if isinstance(item, Mapping)]
    pages_in = [item for item in (document.get("pages") if isinstance(document, Mapping) else ()) or () if isinstance(item, Mapping)]
    blocks_by_section: dict[str, list[str]] = {}
    render_blocks: list[RenderBlock] = []
    for item in blocks_in:
        section_id = str(item.get("section_id") or "")
        block_id = str(item.get("block_id") or "")
        render_blocks.append(
            RenderBlock(
                block_id=block_id,
                section_id=section_id,
                block_type=str(item.get("block_type") or ""),
                source_refs=tuple(str(ref) for ref in item.get("source_refs") or ()),
                asset_ids=tuple(str(ref) for ref in item.get("asset_ids") or ()),
            )
        )
        if section_id and block_id:
            blocks_by_section.setdefault(section_id, []).append(block_id)
    pages = tuple(
        RenderPage(
            page_id=str(item.get("page_id") or f"PAGE-{index}"),
            sequence=int(item.get("sequence") or index),
            section_id=str(item.get("section_id") or ""),
            block_ids=tuple(blocks_by_section.get(str(item.get("section_id") or ""), ())),
        )
        for index, item in enumerate(pages_in)
    )
    style = RenderStyle(
        theme_id=str(theme.get("theme_id") or ""),
        palette_id=str(theme.get("palette_id") or ""),
        spacing_id=str(theme.get("spacing_id") or ""),
        typography_id=str(theme.get("typography_id") or ""),
        icon_set_id=str(theme.get("icon_set_id") or ""),
    )
    resolved_assets = tuple(assets) if assets is not None else ()
    return RenderModel(
        document_id=str((document or {}).get("document_id") or "DOC-unknown"),
        pages=pages,
        blocks=tuple(render_blocks),
        assets=resolved_assets,
        styles=style,
        metadata={
            "layout_version": str(layout.get("layout_version") or ""),
            "render_version": context.render_version,
            "renderer_id": context.renderer_id,
            "filesystem": False,
            "persistence": False,
            "printing": False,
        },
    )
