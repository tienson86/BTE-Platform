"""Search models and deterministic I/O helpers."""

from __future__ import annotations

import hashlib
import json
import logging
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(slots=True)
class SearchDocument:
    """Indexed searchable document."""

    doc_id: str
    kind: str
    canonical_name: str
    aliases: list[str] = field(default_factory=list)
    category: str = ""
    layer: str = ""
    path: str = ""
    text: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Serialize document."""
        return asdict(self)


@dataclass(slots=True)
class SearchHit:
    """A single search hit."""

    doc_id: str
    kind: str
    canonical_name: str
    score: float
    match_type: str
    path: str = ""
    category: str = ""
    snippet: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Serialize hit."""
        return asdict(self)


@dataclass(slots=True)
class SearchResult:
    """Aggregated search response."""

    query: str
    mode: str
    hits: list[SearchHit]
    elapsed_ms: float
    total: int

    def to_dict(self) -> dict[str, Any]:
        """Serialize result."""
        return {
            "query": self.query,
            "mode": self.mode,
            "total": self.total,
            "elapsed_ms": self.elapsed_ms,
            "hits": [hit.to_dict() for hit in self.hits],
        }


def canonical_json_dumps(payload: Any) -> str:
    """Deterministic JSON text."""
    return json.dumps(
        payload,
        ensure_ascii=False,
        indent=2,
        sort_keys=True,
        separators=(",", ": "),
    ) + "\n"


def write_json(path: Path, payload: Any) -> str:
    """Write deterministic JSON and return SHA-256."""
    path.parent.mkdir(parents=True, exist_ok=True)
    text = canonical_json_dumps(payload)
    path.write_text(text, encoding="utf-8", newline="\n")
    logger.debug("Wrote %s", path)
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_json(path: Path) -> Any:
    """Read UTF-8 JSON."""
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def sha256_file(path: Path) -> str:
    """File SHA-256."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
