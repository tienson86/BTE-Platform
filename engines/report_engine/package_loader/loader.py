"""Report Package loader stub. No packages are released in RE-1."""

from __future__ import annotations

import logging

from engines.report_engine.exceptions.foundation_error import ReportPackageNotReleasedError
from engines.report_engine.package_loader.interfaces import LoadedReportPackage

logger = logging.getLogger(__name__)


class ReportPackageLoader:
    """Prepare package admission. RE-1 loads nothing."""

    def list_available(self) -> tuple[str, ...]:
        """Return an empty catalog until Report Packages are released."""
        return ()

    def load(
        self,
        package_id: str,
        *,
        version_constraint: str | None = None,
    ) -> LoadedReportPackage:
        """Fail closed. Report Packages are not released in RE-1."""
        logger.info(
            "report_package_not_released",
            extra={"package_id": package_id, "version_constraint": version_constraint},
        )
        raise ReportPackageNotReleasedError(f"no_report_packages_released:{package_id}")
