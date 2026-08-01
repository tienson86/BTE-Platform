"""Interpretation context history for revision auditing."""

from __future__ import annotations

from dataclasses import dataclass

from engines.interpretation_engine.context.revision import ContextRevision
from engines.interpretation_engine.context.snapshot import ContextSnapshot
from engines.interpretation_engine.exceptions.context_error import InterpretationContextError


@dataclass(frozen=True, slots=True)
class ContextHistory:
    """Immutable append-only history of context revisions and snapshots."""

    context_id: str
    revisions: tuple[ContextRevision, ...] = ()
    snapshots: tuple[ContextSnapshot, ...] = ()

    def with_revision(self, revision: ContextRevision) -> ContextHistory:
        """Return a new history with an appended revision."""
        if revision.context_id != self.context_id:
            raise InterpretationContextError(
                f"revision_context_mismatch:{revision.context_id}:{self.context_id}"
            )
        if self.revisions and revision.revision_number <= self.revisions[-1].revision_number:
            raise InterpretationContextError(
                f"revision_number_not_monotonic:{revision.revision_number}"
            )
        return ContextHistory(
            context_id=self.context_id,
            revisions=self.revisions + (revision,),
            snapshots=self.snapshots,
        )

    def with_snapshot(self, snapshot: ContextSnapshot) -> ContextHistory:
        """Return a new history with an appended snapshot."""
        if snapshot.context_id != self.context_id:
            raise InterpretationContextError(
                f"snapshot_context_mismatch:{snapshot.context_id}:{self.context_id}"
            )
        return ContextHistory(
            context_id=self.context_id,
            revisions=self.revisions,
            snapshots=self.snapshots + (snapshot,),
        )

    def latest_revision(self) -> ContextRevision | None:
        """Return the most recent revision, if any."""
        if not self.revisions:
            return None
        return self.revisions[-1]

    def latest_snapshot(self) -> ContextSnapshot | None:
        """Return the most recent snapshot, if any."""
        if not self.snapshots:
            return None
        return self.snapshots[-1]

    def revision_count(self) -> int:
        """Return the number of recorded revisions."""
        return len(self.revisions)
