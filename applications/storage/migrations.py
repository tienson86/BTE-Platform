"""Migration framework stub (no data migration in WP12)."""

from __future__ import annotations

import logging
from dataclasses import dataclass, field
from typing import Callable

logger = logging.getLogger("bte.applications.storage.migrations")

MigrationFn = Callable[[], None]


@dataclass(slots=True)
class Migration:
    """A named, ordered schema migration step."""

    version: str
    description: str
    apply: MigrationFn


@dataclass
class MigrationRunner:
    """
    Lightweight migration registry.

    WP12 prepares the framework only — no automatic data migration.
    """

    migrations: list[Migration] = field(default_factory=list)
    applied: list[str] = field(default_factory=list)

    def register(self, migration: Migration) -> None:
        """Register a migration definition."""
        self.migrations.append(migration)
        self.migrations.sort(key=lambda item: item.version)

    def pending(self) -> list[Migration]:
        """Migrations not yet marked applied."""
        done = set(self.applied)
        return [item for item in self.migrations if item.version not in done]

    def run_pending(self, *, dry_run: bool = True) -> list[str]:
        """
        Run pending migrations.

        Default ``dry_run=True`` — WP12 does not migrate production data.
        """
        ran: list[str] = []
        for migration in self.pending():
            logger.info(
                "migration %s (%s) dry_run=%s",
                migration.version,
                migration.description,
                dry_run,
            )
            if not dry_run:
                migration.apply()
            self.applied.append(migration.version)
            ran.append(migration.version)
        return ran


def build_default_runner() -> MigrationRunner:
    """
    Default registry for future schema steps.

    Includes a no-op placeholder so the framework is exercisable in tests.
    """
    runner = MigrationRunner()
    runner.register(
        Migration(
            version="0001_init",
            description="Initialize persistence layer (no-op placeholder)",
            apply=lambda: None,
        )
    )
    return runner
