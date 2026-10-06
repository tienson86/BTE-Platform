"""Durable childbirth profiles, written atomically without recomputation."""

from __future__ import annotations

import os
import re
from datetime import datetime, timezone
from pathlib import Path
from threading import RLock
from typing import Any
from uuid import uuid4

from pydantic import BaseModel


class ChildbirthProfile(BaseModel):
    consultation_id: str
    created_at: str
    saved_at: str | None = None
    input: dict[str, Any]
    result: dict[str, Any]


class JsonChildbirthRepository:
    """One file per profile keeps independent consultations from overwriting each other."""

    def __init__(self, directory: Path) -> None:
        self.directory = directory
        self._lock = RLock()

    @classmethod
    def from_environment(cls) -> JsonChildbirthRepository:
        configured = os.getenv("BTE_CHILDBIRTH_DATA_DIR", "").strip()
        default = Path(__file__).resolve().parents[2] / "applications" / "data" / "childbirth"
        return cls(Path(configured).expanduser() if configured else default)

    def create(self, inputs: dict[str, Any], result: dict[str, Any]) -> ChildbirthProfile:
        profile = ChildbirthProfile(
            consultation_id=f"CB-{uuid4().hex}",
            created_at=datetime.now(timezone.utc).isoformat(),
            input=inputs,
            result=result,
        )
        self._write(profile)
        return profile

    def get(self, consultation_id: str) -> ChildbirthProfile:
        path = self._path(consultation_id)
        try:
            return ChildbirthProfile.model_validate_json(path.read_bytes())
        except FileNotFoundError as exc:
            raise KeyError(consultation_id) from exc

    def save(self, consultation_id: str) -> ChildbirthProfile:
        with self._lock:
            profile = self.get(consultation_id)
            if profile.saved_at is None:
                profile.saved_at = datetime.now(timezone.utc).isoformat()
                self._write(profile)
            return profile

    def history(self) -> list[ChildbirthProfile]:
        profiles = [self.get(path.stem) for path in self.directory.glob("CB-*.json")]
        return sorted(
            (profile for profile in profiles if profile.saved_at),
            key=lambda profile: (profile.saved_at, profile.consultation_id), reverse=True,
        )

    def _path(self, consultation_id: str) -> Path:
        if not re.fullmatch(r"CB-[a-f0-9]{32}", consultation_id):
            raise KeyError(consultation_id)
        return self.directory / f"{consultation_id}.json"

    def _write(self, profile: ChildbirthProfile) -> None:
        with self._lock:
            path = self._path(profile.consultation_id)
            self.directory.mkdir(parents=True, exist_ok=True)
            temporary = path.with_suffix(f".{uuid4().hex}.tmp")
            try:
                temporary.write_text(profile.model_dump_json(indent=2), encoding="utf-8")
                temporary.replace(path)
            finally:
                temporary.unlink(missing_ok=True)
