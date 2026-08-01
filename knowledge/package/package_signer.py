"""Package integrity signer (deterministic HMAC-SHA256)."""

from __future__ import annotations

import hashlib
import hmac
from typing import Any

from knowledge.package.constants import SIGNING_KEY_ID, SIGNING_KEY_MATERIAL
from knowledge.package.io_utils import canonical_json_dumps, sha256_text


class PackageSigner:
    """Create and verify deterministic package integrity signatures."""

    def __init__(self, key_material: str = SIGNING_KEY_MATERIAL) -> None:
        """Initialize signer with integrity key material."""
        self.key_material = key_material.encode("utf-8")
        self.key_id = SIGNING_KEY_ID

    def sign_payload(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Sign a JSON-serializable payload and return signature metadata."""
        canonical = canonical_json_dumps(payload)
        digest = sha256_text(canonical)
        signature = hmac.new(
            self.key_material,
            canonical.encode("utf-8"),
            hashlib.sha256,
        ).hexdigest()
        return {
            "key_id": self.key_id,
            "algorithm": "HMAC-SHA256",
            "content_sha256": digest,
            "signature": signature,
        }

    def verify_payload(self, payload: dict[str, Any], signature_block: dict[str, Any]) -> bool:
        """Verify a signature block against a payload."""
        expected = self.sign_payload(payload)
        return (
            expected["content_sha256"] == signature_block.get("content_sha256")
            and hmac.compare_digest(
                expected["signature"],
                str(signature_block.get("signature") or ""),
            )
        )

    def sign_files(self, file_checksums: dict[str, str]) -> dict[str, Any]:
        """Sign a deterministic map of relative_path -> sha256."""
        payload = {"files": dict(sorted(file_checksums.items()))}
        return self.sign_payload(payload)
