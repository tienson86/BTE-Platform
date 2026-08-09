"""Pure HTML renderer. No web server."""

from __future__ import annotations

from html import escape

from engines.report_engine.rendering.render_model import RenderArtifact, RenderModel
from engines.report_engine.rendering.renderer_registry import MIME_HTML, RENDERER_HTML


class HtmlRenderer:
    """Render the canonical model as a pure HTML document string."""

    renderer_id: str = RENDERER_HTML
    mime_type: str = MIME_HTML

    def render(self, model: RenderModel) -> RenderArtifact:
        """Return deterministic HTML with identities only. No CSS stylesheet."""
        blocks_by_id = {item.block_id: item for item in model.blocks}
        sections: list[str] = []
        for page in model.pages:
            block_html = []
            for block_id in page.block_ids:
                block = blocks_by_id.get(block_id)
                if block is None:
                    continue
                refs = " ".join(escape(ref) for ref in block.source_refs)
                assets = " ".join(escape(asset_id) for asset_id in block.asset_ids)
                block_html.append(
                    f'<div data-block="{escape(block.block_id)}" data-type="{escape(block.block_type)}" '
                    f'data-refs="{refs}" data-assets="{assets}"></div>'
                )
            inner = "".join(block_html)
            sections.append(
                f'<section id="{escape(page.section_id)}" data-page="{escape(page.page_id)}">{inner}</section>'
            )
        body = "".join(sections)
        html = (
            "<!DOCTYPE html><html><head><meta charset=\"utf-8\"/>"
            f"<meta name=\"theme\" content=\"{escape(model.styles.theme_id)}\"/>"
            f"<title>{escape(model.document_id)}</title></head>"
            f"<body data-document=\"{escape(model.document_id)}\">{body}</body></html>"
        )
        return RenderArtifact(
            artifact_id="ART-html-1",
            renderer=self.renderer_id,
            mime_type=self.mime_type,
            content=html,
            metadata={"format": RENDERER_HTML, "web_server": False},
            assets=tuple(item.to_dict() for item in model.assets),
        )
