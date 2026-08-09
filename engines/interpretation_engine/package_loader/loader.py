"""Interpretation Package loader stub. No packages are released in IE-1."""

from __future__ import annotations

import logging

from engines.interpretation_engine.exceptions.foundation_error import (
    InterpretationPackageNotReleasedError,
)
from engines.interpretation_engine.package_loader.interfaces import LoadedInterpretationPackage

logger = logging.getLogger(__name__)


class InterpretationPackageLoader:
    """Prepare package admission. IE-1 loads nothing."""

    def list_available(self) -> tuple[str, ...]:
        """Return an empty catalog until Interpretation Packages are released."""
        return ()

    def load(
        self,
        package_id: str,
        *,
        version_constraint: str | None = None,
    ) -> LoadedInterpretationPackage:
        """Fail closed. Interpretation Packages are not released in IE-1."""
        logger.info(
            "interpretation_package_not_released",
            extra={"package_id": package_id, "version_constraint": version_constraint},
        )
        raise InterpretationPackageNotReleasedError(
            f"no_interpretation_packages_released:{package_id}"
        )
