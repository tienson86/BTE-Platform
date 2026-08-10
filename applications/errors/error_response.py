"""Build canonical public error payloads without leaking internals."""

from __future__ import annotations

import re
from datetime import datetime, timezone
from typing import Any

from applications.contracts.error_models import CanonicalError, ErrorDetails
from applications.errors.error_codes import (
    HTTP_STATUS_BY_CODE,
    INTERNAL_ERROR,
    SAFE_PUBLIC_MESSAGES,
)

_PATH_PATTERN = re.compile(
    r"(?:[A-Za-z]:\\|/)(?:Users|home|tmp|var|opt|app|Windows|Documents)[^\s\"']*",
    re.IGNORECASE,
)
_TRACE_KEYS = frozenset(
    {"traceback", "stack", "stacktrace", "exc_info", "exception", "pathname", "filename"}
)


def utc_now() -> datetime:
    """Return a timezone-aware UTC timestamp."""
    return datetime.now(timezone.utc)


def sanitize_text(value: str) -> str:
    """Remove filesystem-like fragments from public text."""
    return _PATH_PATTERN.sub("[redacted]", value)


def sanitize_details(details: ErrorDetails | dict[str, Any] | None) -> ErrorDetails | None:
    """Drop unsafe keys and redact path-like strings."""
    if details is None:
        return None
    if isinstance(details, ErrorDetails):
        payload = details.model_dump()
    else:
        payload = dict(details)
    extra = payload.get("extra")
    if isinstance(extra, dict):
        cleaned_extra = {
            key: value
            for key, value in extra.items()
            if key.lower() not in _TRACE_KEYS
        }
        payload["extra"] = cleaned_extra or None
    context = payload.get("context") or []
    payload["context"] = [sanitize_text(str(item)) for item in context]
    if payload.get("reason"):
        payload["reason"] = sanitize_text(str(payload["reason"]))
    if payload.get("field"):
        payload["field"] = sanitize_text(str(payload["field"]))
    return ErrorDetails.model_validate(payload)


class PublicServiceError(Exception):
    """Service-layer error mapped to a canonical public error body."""

    def __init__(
        self,
        code: str,
        message: str | None = None,
        *,
        details: ErrorDetails | dict[str, Any] | None = None,
        status_code: int | None = None,
    ) -> None:
        public_message = sanitize_text(message or SAFE_PUBLIC_MESSAGES.get(code, SAFE_PUBLIC_MESSAGES[INTERNAL_ERROR]))
        super().__init__(public_message)
        self.code = code
        self.public_message = public_message
        self.details = sanitize_details(details)
        self.status_code = status_code or HTTP_STATUS_BY_CODE.get(code, 500)

    def to_model(self, request_id: str, timestamp: datetime | None = None) -> CanonicalError:
        """Convert to the public error contract."""
        return CanonicalError(
            code=self.code,
            message=self.public_message,
            details=self.details,
            request_id=request_id,
            timestamp=timestamp or utc_now(),
        )


def build_error_response(
    *,
    code: str,
    request_id: str,
    message: str | None = None,
    details: ErrorDetails | dict[str, Any] | None = None,
    timestamp: datetime | None = None,
) -> CanonicalError:
    """Build a canonical error body from a public code."""
    return PublicServiceError(code, message, details=details).to_model(
        request_id=request_id,
        timestamp=timestamp,
    )
