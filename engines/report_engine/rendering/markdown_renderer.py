"""Pure Markdown renderer. No filesystem writes."""

from __future__ import annotations

from engines.report_engine.rendering.render_model import RenderArtifact, RenderModel
from engines.report_engine.rendering.renderer_registry import MIME_MARKDOWN, RENDERER_MARKDOWN


class MarkdownRenderer:
    """Render the canonical model as a pure Markdown document string."""

    renderer_id: str = RENDERER_MARKDOWN
    mime_type: str = MIME_MARKDOWN

    def render(self, model: RenderModel) -> RenderArtifact:
        """Return deterministic Markdown from layout identities."""
        blocks_by_id = {item.block_id: item for item in model.blocks}
        lines = [f"# {model.document_id}", "", f"theme: {model.styles.theme_id}", ""]
        for page in model.pages:
            lines.append(f"## {page.section_id}")
            for block_id in page.block_ids:
                block = blocks_by_id.get(block_id)
                if block is None:
                    continue
                refs = ",".join(block.source_refs)
                lines.append(f"- {block.block_type}: {block.block_id} [{refs}]")
            lines.append("")
        return RenderArtifact(
            artifact_id="ART-markdown-1",
            renderer=self.renderer_id,
            mime_type=self.mime_type,
            content="\n".join(lines).rstrip() + "\n",
            metadata={"format": RENDERER_MARKDOWN, "filesystem": False},
            assets=tuple(item.to_dict() for item in model.assets),
        )
