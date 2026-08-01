"""Knowledge Search Engine — index builder and unified query API."""

from __future__ import annotations

import logging
import os
import time
from pathlib import Path
from typing import Any

from knowledge.search.constants import (
    ACADEMIC_HARD_DEPS,
    DEFAULT_LIMIT,
    DEFAULT_TIMESTAMP,
    ENGINE_VERSION,
    FUZZY_THRESHOLD,
    PACK01_RECORDS,
    REGISTRY_DOMAINS,
    SCHEMA_VERSION,
)
from knowledge.search.context_search import ContextSearch
from knowledge.search.entity_search import EntitySearch
from knowledge.search.matching import contains_match, exact_match, fuzzy_ratio, prefix_match
from knowledge.search.models import SearchDocument, SearchHit, SearchResult, read_json, write_json
from knowledge.search.registry_search import RegistrySearch
from knowledge.search.relationship_search import RelationshipSearch
from knowledge.search.rule_search import RuleSearch

logger = logging.getLogger(__name__)


class SearchEngine:
    """Unified deterministic search engine for Pack 01 knowledge assets."""

    def __init__(
        self,
        project_root: Path | None = None,
        *,
        timestamp: str | None = None,
    ) -> None:
        """Initialize engine rooted at the BTE project."""
        self.project_root = (
            project_root.resolve()
            if project_root is not None
            else Path(__file__).resolve().parents[2]
        )
        self.timestamp = (
            timestamp
            or os.environ.get("SOURCE_DATE_EPOCH_ISO")
            or DEFAULT_TIMESTAMP
        )
        self.output_dir = self.project_root / "knowledge" / "search"
        self.documents: list[SearchDocument] = []
        self._by_id: dict[str, SearchDocument] = {}
        self.entity_search = EntitySearch([])
        self.relationship_search = RelationshipSearch([])
        self.rule_search = RuleSearch([])
        self.context_search = ContextSearch([])
        self.registry_search = RegistrySearch([])

    def build_index(self) -> dict[str, Any]:
        """Build in-memory index and persist search_index/statistics JSON."""
        self.documents = self._collect_documents()
        self._by_id = {doc.doc_id: doc for doc in self.documents}
        self.entity_search = EntitySearch(self.documents)
        self.relationship_search = RelationshipSearch(self.documents)
        self.rule_search = RuleSearch(self.documents)
        self.context_search = ContextSearch(self.documents)
        self.registry_search = RegistrySearch(self.documents)

        index_payload = {
            "artifact": "search_index",
            "schema_version": SCHEMA_VERSION,
            "engine_version": ENGINE_VERSION,
            "timestamp": self.timestamp,
            "document_count": len(self.documents),
            "documents": [doc.to_dict() for doc in self.documents],
            "indexes": {
                "by_id": sorted(self._by_id.keys()),
                "by_kind": self._index_by_kind(),
                "by_category": self._index_by_category(),
                "dependency_edges": [
                    {"source": source, "target": target}
                    for source, target in ACADEMIC_HARD_DEPS
                ],
            },
        }
        statistics = self._build_statistics()
        write_json(self.output_dir / "search_index.json", index_payload)
        write_json(self.output_dir / "search_statistics.json", statistics)
        summary = {
            "status": "SEARCH_READY",
            "document_count": len(self.documents),
            "timestamp": self.timestamp,
            "statistics": statistics,
        }
        write_json(self.output_dir / "search_build_summary.json", summary)
        logger.info("Search index built: %s documents", len(self.documents))
        return summary

    def load_index(self) -> None:
        """Load previously generated search_index.json into memory."""
        path = self.output_dir / "search_index.json"
        if not path.is_file():
            self.build_index()
            return
        payload = read_json(path)
        docs = []
        for item in payload.get("documents", []):
            docs.append(
                SearchDocument(
                    doc_id=str(item["doc_id"]),
                    kind=str(item.get("kind", "")),
                    canonical_name=str(item.get("canonical_name", "")),
                    aliases=list(item.get("aliases") or []),
                    category=str(item.get("category") or ""),
                    layer=str(item.get("layer") or ""),
                    path=str(item.get("path") or ""),
                    text=str(item.get("text") or ""),
                    metadata=dict(item.get("metadata") or {}),
                )
            )
        self.documents = docs
        self._by_id = {doc.doc_id: doc for doc in docs}
        self.entity_search = EntitySearch(docs)
        self.relationship_search = RelationshipSearch(docs)
        self.rule_search = RuleSearch(docs)
        self.context_search = ContextSearch(docs)
        self.registry_search = RegistrySearch(docs)

    def search(
        self,
        query: str,
        *,
        mode: str = "exact",
        limit: int = DEFAULT_LIMIT,
        kind: str | None = None,
    ) -> SearchResult:
        """Run a deterministic search query."""
        started = time.perf_counter()
        if not self.documents:
            self.load_index()
        normalized_mode = mode.strip().lower()
        q = query.strip()
        if not q:
            elapsed = (time.perf_counter() - started) * 1000.0
            return SearchResult(query=query, mode=normalized_mode, hits=[], elapsed_ms=elapsed, total=0)

        if normalized_mode == "ontology":
            hits = self._ontology_search(q, limit=limit)
        elif normalized_mode == "dependency":
            hits = self._dependency_search(q, limit=limit)
        elif normalized_mode == "relationship":
            hits = self.relationship_search.search(q, mode="relationship", limit=limit)
        elif kind == "rule":
            hits = self.rule_search.search(q, mode=normalized_mode, limit=limit)
        elif kind == "context":
            hits = self.context_search.search(q, mode=normalized_mode, limit=limit)
        elif kind == "registry":
            hits = self.registry_search.search(q, mode=normalized_mode, limit=limit)
        elif kind in {"entity", "concept"}:
            hits = self.entity_search.search(q, mode=normalized_mode, limit=limit)
        else:
            hits = self._unified_search(q, mode=normalized_mode, limit=limit)

        if kind and normalized_mode not in {"ontology", "dependency", "relationship"}:
            hits = [hit for hit in hits if hit.kind == kind or hit.kind.startswith(kind)]

        elapsed = (time.perf_counter() - started) * 1000.0
        # Round for stable reporting without hurting measured budget checks.
        elapsed_rounded = round(elapsed, 4)
        return SearchResult(
            query=query,
            mode=normalized_mode,
            hits=hits[:limit],
            elapsed_ms=elapsed_rounded,
            total=len(hits[:limit]),
        )

    def exact(self, query: str, *, limit: int = DEFAULT_LIMIT) -> SearchResult:
        """Exact search convenience API."""
        return self.search(query, mode="exact", limit=limit)

    def prefix(self, query: str, *, limit: int = DEFAULT_LIMIT) -> SearchResult:
        """Prefix search convenience API."""
        return self.search(query, mode="prefix", limit=limit)

    def fuzzy(self, query: str, *, limit: int = DEFAULT_LIMIT) -> SearchResult:
        """Fuzzy search convenience API."""
        return self.search(query, mode="fuzzy", limit=limit)

    def _unified_search(self, query: str, *, mode: str, limit: int) -> list[SearchHit]:
        hits: list[SearchHit] = []
        q_lower = query.lower()
        for doc in self.documents:
            if mode == "fuzzy":
                # Cheap prefilter before difflib.
                identity = f"{doc.doc_id} {doc.canonical_name} {' '.join(doc.aliases)}".lower()
                if q_lower[:3] not in identity and not any(
                    token in identity for token in q_lower.split() if token
                ):
                    continue
            score, match_type = self._score(query, doc, mode=mode)
            if score <= 0:
                continue
            hits.append(
                SearchHit(
                    doc_id=doc.doc_id,
                    kind=doc.kind,
                    canonical_name=doc.canonical_name,
                    score=score,
                    match_type=match_type,
                    path=doc.path,
                    category=doc.category,
                    snippet=doc.canonical_name,
                )
            )
        hits.sort(key=lambda item: (-item.score, item.doc_id))
        return hits[:limit]

    def _ontology_search(self, query: str, *, limit: int) -> list[SearchHit]:
        docs = [doc for doc in self.documents if doc.kind.startswith("ontology")]
        hits: list[SearchHit] = []
        for doc in docs:
            score, match_type = self._score(query, doc, mode="contains")
            if score <= 0:
                # also allow exact/prefix for ontology mode
                score, match_type = self._score(query, doc, mode="prefix")
            if score <= 0:
                continue
            hits.append(
                SearchHit(
                    doc_id=doc.doc_id,
                    kind=doc.kind,
                    canonical_name=doc.canonical_name,
                    score=score,
                    match_type=match_type or "ontology",
                    path=doc.path,
                    category=doc.category,
                    snippet=doc.canonical_name,
                )
            )
        hits.sort(key=lambda item: (-item.score, item.doc_id))
        return hits[:limit]

    def _dependency_search(self, query: str, *, limit: int) -> list[SearchHit]:
        hits: list[SearchHit] = []
        q = query.strip().upper()
        for source, target in ACADEMIC_HARD_DEPS:
            if q in {source, target} or q.lower() in source.lower() or q.lower() in target.lower():
                edge_id = f"{source}->{target}"
                hits.append(
                    SearchHit(
                        doc_id=edge_id,
                        kind="dependency",
                        canonical_name=edge_id,
                        score=3.0 if q in {source, target} else 1.5,
                        match_type="dependency",
                        path="knowledge/search/search_index.json",
                        category="hard_dependency",
                        snippet=f"{source} depends on {target}",
                    )
                )
        # Also include dependency docs if present.
        for doc in self.documents:
            if doc.kind != "dependency":
                continue
            score, match_type = self._score(query, doc, mode="contains")
            if score > 0:
                hits.append(
                    SearchHit(
                        doc_id=doc.doc_id,
                        kind=doc.kind,
                        canonical_name=doc.canonical_name,
                        score=score,
                        match_type=match_type,
                        path=doc.path,
                        category=doc.category,
                        snippet=doc.text or doc.canonical_name,
                    )
                )
        hits.sort(key=lambda item: (-item.score, item.doc_id))
        return hits[:limit]

    def _score(self, query: str, doc: SearchDocument, *, mode: str) -> tuple[float, str]:
        # Prefer short identity fields for fuzzy to keep latency deterministic.
        identity_fields = [doc.doc_id, doc.canonical_name, *doc.aliases]
        all_fields = identity_fields + [doc.category, doc.layer, doc.text]
        best = 0.0
        match_type = mode
        q_tokens = [token for token in query.lower().split() if token]

        if mode == "fuzzy":
            for field in identity_fields:
                if not field:
                    continue
                field_l = field.lower()
                if q_tokens and all(token in field_l for token in q_tokens):
                    best = max(best, 0.9)
                    match_type = "fuzzy"
                    continue
                ratio = fuzzy_ratio(query, field)
                if ratio >= FUZZY_THRESHOLD:
                    best = max(best, ratio)
                    match_type = "fuzzy"
            return best, match_type

        for field in all_fields:
            if not field:
                continue
            if mode == "exact" and exact_match(query, field):
                best = max(best, 3.0 if exact_match(query, doc.doc_id) else 2.5)
                match_type = "exact"
            elif mode == "prefix" and prefix_match(query, field):
                best = max(best, 2.0)
                match_type = "prefix"
            elif contains_match(query, field):
                best = max(best, 1.5)
                match_type = "contains"
        return best, match_type

    def _collect_documents(self) -> list[SearchDocument]:
        documents: list[SearchDocument] = []

        # Knowledge Record entities / concepts / context / relationships / rules.
        for record in PACK01_RECORDS:
            kind = "concept"
            category = record["category"]
            if category == "Context":
                kind = "context"
            elif category == "Relationship":
                kind = "relationship"
            elif category in {"Composite Rule"}:
                kind = "rule"
            elif category in {"Entity", "Composition", "Composite Entity"}:
                kind = "entity"
            path = (
                "knowledge/bazi/01_fundamental_knowledge/records/"
                f"{record['filename']}"
            )
            documents.append(
                SearchDocument(
                    doc_id=record["record_id"],
                    kind=kind,
                    canonical_name=record["canonical_name"],
                    aliases=[record["record_id"], record["category"], record["layer"]],
                    category=category,
                    layer=record["layer"],
                    path=path,
                    text=f"{record['canonical_name']} {record['category']} {record['layer']}",
                    metadata={"pack_id": "PACK_01"},
                )
            )

        # Ontology classes and entity/relationship types.
        ontology_dir = self.project_root / "knowledge" / "ontology"
        class_path = ontology_dir / "ontology_classes.json"
        if class_path.is_file():
            for item in read_json(class_path).get("classes", []):
                class_id = str(item.get("id") or "")
                if not class_id:
                    continue
                name = str(item.get("canonical_name") or class_id)
                documents.append(
                    SearchDocument(
                        doc_id=class_id,
                        kind="ontology_class",
                        canonical_name=name,
                        aliases=[class_id],
                        category="ontology",
                        path="knowledge/ontology/ontology_classes.json",
                        text=str(item.get("description") or name),
                    )
                )
        entity_path = ontology_dir / "entity_types.json"
        if entity_path.is_file():
            for item in read_json(entity_path).get("entity_types", []):
                entity_id = str(item.get("id") or "")
                if not entity_id:
                    continue
                name = str(item.get("canonical_name") or entity_id)
                documents.append(
                    SearchDocument(
                        doc_id=entity_id,
                        kind="ontology_entity",
                        canonical_name=name,
                        aliases=[entity_id],
                        category="ontology_entity",
                        path="knowledge/ontology/entity_types.json",
                        text=str(item.get("description") or name),
                        metadata={"ontology_class_id": item.get("ontology_class_id")},
                    )
                )
        rel_path = ontology_dir / "relationship_types.json"
        if rel_path.is_file():
            for item in read_json(rel_path).get("relationship_types", []):
                rel_id = str(item.get("id") or "")
                if not rel_id:
                    continue
                name = str(item.get("canonical_name") or rel_id)
                documents.append(
                    SearchDocument(
                        doc_id=rel_id,
                        kind="relationship",
                        canonical_name=name,
                        aliases=[rel_id],
                        category="ontology_relationship",
                        path="knowledge/ontology/relationship_types.json",
                        text=str(item.get("description") or name),
                    )
                )

        # Validation rules.
        validation_dir = self.project_root / "knowledge" / "validation"
        if validation_dir.is_dir():
            for path in sorted(validation_dir.glob("*validator*.json")):
                payload = read_json(path)
                for rule in payload.get("rules", []):
                    if not isinstance(rule, dict):
                        continue
                    code = str(rule.get("code") or rule.get("rule_id") or "")
                    if not code:
                        continue
                    title = str(rule.get("title") or rule.get("statement") or code)
                    documents.append(
                        SearchDocument(
                            doc_id=code,
                            kind="rule",
                            canonical_name=title,
                            aliases=[code],
                            category=str(rule.get("severity") or "rule"),
                            path=f"knowledge/validation/{path.name}",
                            text=str(rule.get("description") or title),
                        )
                    )

        # Registry domains / namespaces / object types.
        for domain in REGISTRY_DOMAINS:
            documents.append(
                SearchDocument(
                    doc_id=f"REGDOM-{domain}",
                    kind="registry_domain",
                    canonical_name=domain,
                    aliases=[domain, f"REGDOM-{domain}"],
                    category="registry",
                    path=f"knowledge/registry/{domain}/{domain}.json",
                    text=domain.replace("_", " "),
                )
            )
        ns_path = (
            self.project_root
            / "knowledge"
            / "registry"
            / "global_registry"
            / "namespace_registry.json"
        )
        if ns_path.is_file():
            for record in read_json(ns_path).get("records", []):
                namespace = str(record.get("namespace") or "")
                if not namespace:
                    continue
                documents.append(
                    SearchDocument(
                        doc_id=f"NS-{namespace}",
                        kind="registry_namespace",
                        canonical_name=namespace,
                        aliases=[namespace, str(record.get("prefix") or "")],
                        category="namespace",
                        path="knowledge/registry/global_registry/namespace_registry.json",
                        text=str(record.get("description") or namespace),
                    )
                )
        ot_path = (
            self.project_root
            / "knowledge"
            / "registry"
            / "global_registry"
            / "object_type_registry.json"
        )
        if ot_path.is_file():
            for record in read_json(ot_path).get("records", []):
                object_type = str(record.get("object_type") or "")
                if not object_type:
                    continue
                documents.append(
                    SearchDocument(
                        doc_id=f"OTYPE-{object_type}",
                        kind="registry_object_type",
                        canonical_name=object_type,
                        aliases=[object_type, str(record.get("object_id_prefix") or "")],
                        category="object_type",
                        path="knowledge/registry/global_registry/object_type_registry.json",
                        text=object_type,
                        metadata={"namespace": record.get("namespace")},
                    )
                )

        # Dependency edge documents.
        for idx, (source, target) in enumerate(ACADEMIC_HARD_DEPS, start=1):
            documents.append(
                SearchDocument(
                    doc_id=f"DEP-{idx:06d}",
                    kind="dependency",
                    canonical_name=f"{source}->{target}",
                    aliases=[source, target],
                    category="hard_dependency",
                    path="knowledge/search/search_index.json",
                    text=f"{source} depends on {target}",
                )
            )

        documents.sort(key=lambda doc: doc.doc_id)
        return documents

    def _index_by_kind(self) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        for doc in self.documents:
            result.setdefault(doc.kind, []).append(doc.doc_id)
        return {key: sorted(values) for key, values in sorted(result.items())}

    def _index_by_category(self) -> dict[str, list[str]]:
        result: dict[str, list[str]] = {}
        for doc in self.documents:
            category = doc.category or "uncategorized"
            result.setdefault(category, []).append(doc.doc_id)
        return {key: sorted(values) for key, values in sorted(result.items())}

    def _build_statistics(self) -> dict[str, Any]:
        by_kind = {key: len(values) for key, values in self._index_by_kind().items()}
        return {
            "artifact": "search_statistics",
            "schema_version": SCHEMA_VERSION,
            "engine_version": ENGINE_VERSION,
            "timestamp": self.timestamp,
            "document_count": len(self.documents),
            "by_kind": by_kind,
            "dependency_edge_count": len(ACADEMIC_HARD_DEPS),
            "supported_modes": [
                "exact",
                "prefix",
                "fuzzy",
                "ontology",
                "dependency",
                "relationship",
            ],
        }


def build_search_index(
    project_root: Path | None = None,
    *,
    timestamp: str | None = None,
) -> dict[str, Any]:
    """Convenience API to rebuild the search index."""
    return SearchEngine(project_root=project_root, timestamp=timestamp).build_index()
