"""Template Engine resolver — resolve template references to shells.

Resolves template reference identifiers to ``TemplateRef`` descriptors.
Does not load template bodies. No hard-coded templates.
"""

from __future__ import annotations

from collections.abc import Callable, Mapping

from engines.interpretation_engine.exceptions.template_error import TemplateEngineError
from engines.interpretation_engine.template_engine.loader import Loader
from engines.interpretation_engine.template_engine.metadata import Metadata, TemplateRef


class Resolver:
    """Resolve template reference ids against a caller-supplied catalog.

    Resolution is identity/metadata hydration only.
    """

    def __init__(
        self,
        *,
        ref_provider: Callable[[], tuple[TemplateRef, ...]] | None = None,
        loader: Loader | None = None,
        metadata: Metadata | None = None,
    ) -> None:
        """Initialize resolver collaborators."""
        self._ref_provider = ref_provider or (lambda: ())
        self._loader = loader or Loader()
        self._metadata = metadata or Metadata()

    @property
    def loader(self) -> Loader:
        """Return the bound loader."""
        return self._loader

    @property
    def metadata(self) -> Metadata:
        """Return the bound metadata helper."""
        return self._metadata

    def resolve(self, template_ref: str) -> TemplateRef:
        """Resolve a single template reference by id."""
        if not template_ref or not str(template_ref).strip():
            raise TemplateEngineError("template_ref_required")
        for ref in self._ref_provider():
            if ref.ref_id == template_ref and ref.validate():
                return ref
        raise TemplateEngineError(f"template_ref_not_found:{template_ref}")

    def resolve_many(self, template_refs: tuple[str, ...]) -> tuple[TemplateRef, ...]:
        """Resolve many template references, preserving request order."""
        if not template_refs:
            return ()
        index = {
            ref.ref_id: ref for ref in self._ref_provider() if ref.validate()
        }
        resolved: list[TemplateRef] = []
        missing: list[str] = []
        for ref_id in template_refs:
            ref = index.get(ref_id)
            if ref is None:
                missing.append(ref_id)
                continue
            resolved.append(ref)
        if missing:
            raise TemplateEngineError(f"template_refs_not_found:{','.join(missing)}")
        return tuple(resolved)

    def resolve_by_domain(self, domain: str) -> tuple[TemplateRef, ...]:
        """Resolve all catalog refs for a domain."""
        if not domain:
            raise TemplateEngineError("template_domain_required")
        return tuple(
            ref for ref in self._ref_provider() if ref.domain == domain and ref.validate()
        )

    def resolve_metadata(self, template_ref: str) -> Mapping[str, object]:
        """Resolve normalized metadata for a template reference."""
        return self._metadata.from_ref(self.resolve(template_ref))
