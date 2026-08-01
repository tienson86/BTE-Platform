"""Template Engine loader — load template *reference* descriptors.

Loads descriptor catalogs only. Never loads template bodies.
No hard-coded templates.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from engines.interpretation_engine.exceptions.template_error import TemplateEngineError
from engines.interpretation_engine.template_engine.metadata import TemplateRef

_DEFAULT_VERSION = "0.0.0-architecture"


class Loader:
    """Read-only loader for template reference descriptors.

    Accepts JSON files or in-memory mappings describing ``TemplateRef`` shells.
    Does not read or store template body content.
    """

    def load_from_mapping(self, payload: Mapping[str, Any]) -> tuple[TemplateRef, ...]:
        """Load template references from an in-memory mapping."""
        items = self._extract_items(payload)
        return tuple(self._ref_from_mapping(item) for item in items)

    def load_from_path(self, path: Path) -> tuple[TemplateRef, ...]:
        """Load template references from a JSON descriptor file."""
        if not path.is_file():
            raise TemplateEngineError(f"template_descriptor_path_not_found:{path}")
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise TemplateEngineError(f"template_descriptor_load_failed:{path}") from exc
        if not isinstance(payload, dict):
            raise TemplateEngineError(f"template_descriptor_payload_invalid:{path}")
        return self.load_from_mapping(payload)

    def list_ref_ids(self, path: Path) -> tuple[str, ...]:
        """List template reference identifiers at a descriptor path."""
        refs = self.load_from_path(path)
        return tuple(ref.ref_id for ref in refs)

    def _extract_items(self, payload: Mapping[str, Any]) -> tuple[Mapping[str, Any], ...]:
        """Extract descriptor item list from supported payload shapes."""
        if "entries" in payload and isinstance(payload["entries"], list):
            return tuple(item for item in payload["entries"] if isinstance(item, Mapping))
        if "templates" in payload and isinstance(payload["templates"], list):
            return tuple(
                item for item in payload["templates"] if isinstance(item, Mapping)
            )
        if "ref_id" in payload:
            return (payload,)
        raise TemplateEngineError("template_descriptor_payload_unsupported")

    def _ref_from_mapping(self, item: Mapping[str, Any]) -> TemplateRef:
        """Build a TemplateRef from a descriptor mapping (no body fields)."""
        ref_id = str(item.get("ref_id") or item.get("template_ref") or item.get("id") or "")
        if not ref_id:
            raise TemplateEngineError("template_ref_missing_id")

        # Reject payloads that attempt to embed template bodies.
        for forbidden in ("body", "template", "content", "text", "source"):
            if forbidden in item and item[forbidden] not in (None, "", {}, []):
                raise TemplateEngineError(
                    f"template_body_not_allowed:{forbidden}:{ref_id}"
                )

        slots_raw = item.get("slot_names") or item.get("slots") or ()
        if isinstance(slots_raw, str):
            slot_names = (slots_raw,)
        elif isinstance(slots_raw, (list, tuple)):
            slot_names = tuple(str(slot) for slot in slots_raw)
        else:
            raise TemplateEngineError(f"template_slots_invalid:{ref_id}")

        tags_raw = item.get("tags") or ()
        tags = tuple(tags_raw) if isinstance(tags_raw, (list, tuple)) else ()
        metadata = dict(item.get("metadata") or {})
        for key in ("owner", "module", "path"):
            if key in item and key not in metadata:
                metadata[key] = item[key]

        return TemplateRef(
            ref_id=ref_id,
            version=str(item.get("version") or _DEFAULT_VERSION),
            domain=str(item.get("domain") or ""),
            section=str(item.get("section") or ""),
            locale=str(item.get("locale") or ""),
            status=str(item.get("status") or "draft"),
            slot_names=slot_names,
            tags=tags,
            metadata=metadata,
        )
