"""Registry discovery and query helpers."""

from __future__ import annotations

from typing import Any

from services.registry_exceptions import RegistryQueryError
from services.registry_indexer import RegistryIndexer
from services.registry_loader import RegistryLoader
from services.registry_models import SearchHit


class RegistryQuery:
    """Query and search loaded registry records."""

    def __init__(
        self,
        loader: RegistryLoader,
        indexer: RegistryIndexer | None = None,
    ) -> None:
        """Initialize query service."""
        self.loader = loader
        self.indexer = indexer or RegistryIndexer(loader)

    def list_records(
        self,
        *,
        registry_name: str | None = None,
        status: str | None = None,
        namespace: str | None = None,
        limit: int | None = None,
    ) -> list[SearchHit]:
        """List records with optional filters."""
        hits: list[SearchHit] = []
        for catalog, record in self.loader.iter_records():
            if registry_name and catalog.name != registry_name:
                continue
            identity = record.get("identity", {})
            metadata = record.get("metadata", {})
            obj = record.get("object", {})
            if not isinstance(identity, dict):
                continue
            record_status = (
                str(metadata.get("status", ""))
                if isinstance(metadata, dict)
                else ""
            )
            record_namespace = str(identity.get("namespace", ""))
            if status and record_status != status:
                continue
            if namespace and record_namespace != namespace:
                continue
            hits.append(
                SearchHit(
                    registry_name=catalog.name,
                    registry_id=str(identity.get("registry_id", "")),
                    object_id=str(identity.get("object_id", "")),
                    canonical_name=(
                        str(obj.get("canonical_name", ""))
                        if isinstance(obj, dict)
                        else ""
                    ),
                    status=record_status,
                )
            )
            if limit is not None and len(hits) >= limit:
                break
        return hits

    def get_by_registry_id(self, registry_id: str) -> dict[str, Any] | None:
        """Return a record by registry_id."""
        for _, record in self.loader.iter_records():
            identity = record.get("identity", {})
            if (
                isinstance(identity, dict)
                and str(identity.get("registry_id", "")) == registry_id
            ):
                return record
        return None

    def get_by_object_id(self, object_id: str) -> dict[str, Any] | None:
        """Return a record by object_id."""
        for _, record in self.loader.iter_records():
            identity = record.get("identity", {})
            if (
                isinstance(identity, dict)
                and str(identity.get("object_id", "")) == object_id
            ):
                return record
        return None

    def search(
        self,
        query: str,
        *,
        limit: int = 50,
    ) -> list[SearchHit]:
        """Case-insensitive substring search across key metadata fields."""
        needle = query.strip().lower()
        if not needle:
            raise RegistryQueryError("Search query must not be empty")

        hits: list[SearchHit] = []
        for catalog, record in self.loader.iter_records():
            identity = record.get("identity", {})
            metadata = record.get("metadata", {})
            obj = record.get("object", {})
            classification = record.get("classification", {})
            if not isinstance(identity, dict):
                continue

            haystacks = [
                str(identity.get("registry_id", "")),
                str(identity.get("object_id", "")),
                str(identity.get("namespace", "")),
                str(obj.get("canonical_name", "")) if isinstance(obj, dict) else "",
                str(obj.get("uri", "")) if isinstance(obj, dict) else "",
                str(metadata.get("owner", "")) if isinstance(metadata, dict) else "",
                str(classification.get("domain", ""))
                if isinstance(classification, dict)
                else "",
                str(classification.get("category", ""))
                if isinstance(classification, dict)
                else "",
            ]
            tags = (
                classification.get("tags", [])
                if isinstance(classification, dict)
                else []
            )
            if isinstance(tags, list):
                haystacks.extend(str(tag) for tag in tags)

            joined = " ".join(haystacks).lower()
            if needle not in joined:
                continue

            score = 2.0 if needle in str(identity.get("registry_id", "")).lower() else 1.0
            hits.append(
                SearchHit(
                    registry_name=catalog.name,
                    registry_id=str(identity.get("registry_id", "")),
                    object_id=str(identity.get("object_id", "")),
                    canonical_name=(
                        str(obj.get("canonical_name", ""))
                        if isinstance(obj, dict)
                        else ""
                    ),
                    status=(
                        str(metadata.get("status", ""))
                        if isinstance(metadata, dict)
                        else ""
                    ),
                    score=score,
                )
            )

        hits.sort(key=lambda item: (-item.score, item.registry_id))
        return hits[:limit]
